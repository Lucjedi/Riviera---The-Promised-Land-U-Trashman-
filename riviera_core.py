import json
import re
import struct


TAG_RE = re.compile(r"<([0-9A-Fa-f]{2}|[0-9A-Fa-f]{4})>")
HEXDIGITS = set("0123456789abcdefABCDEF")


class EncodeError(Exception):
    def __init__(self, pos, snippet):
        super().__init__(
            f"caractere/sequência fora da tabela na posição "
            f"{pos}: {snippet!r}"
        )
        self.pos = pos
        self.snippet = snippet


class BuildError(Exception):
    def __init__(self, errors):
        super().__init__(
            f"{len(errors)} entrada(s) com problemas"
        )
        self.errors = errors


class Table:
    def __init__(self):
        self.dec = {}
        self.enc = {}
        self.noncanon = set()
        self.warnings = []
        self.maxlen = 1
        self.path = None

    @classmethod
    def load(cls, path):
        with open(path, "rb") as file:
            raw = file.read()

        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            text = raw.decode("cp1252")

        table = cls()
        table.path = path
        pairs = []

        for number, line in enumerate(text.split("\n"), 1):
            line = line.rstrip("\r")

            if not line.strip():
                continue

            hex_code, separator, character = line.partition(";")
            hex_code = hex_code.strip().lower()

            if (
                not separator
                or len(hex_code) not in (2, 4)
                or not set(hex_code) <= HEXDIGITS
            ):
                table.warnings.append(
                    f"linha {number}: formato inválido ({line!r})"
                )
                continue

            if character == "":
                table.warnings.append(
                    f"linha {number}: caractere vazio para {hex_code}"
                )
                continue

            pairs.append((hex_code, character))

        seen = {}

        for hex_code, character in pairs:
            if (
                hex_code in seen
                and seen[hex_code] != character
            ):
                table.warnings.append(
                    f"código {hex_code} repetido para "
                    f"{seen[hex_code]!r} e {character!r}; "
                    f"vale o último"
                )

            seen[hex_code] = character
            table.dec[hex_code] = character
            table.enc[character] = bytes.fromhex(hex_code)

        for hex_code, character in table.dec.items():
            encoded = table.enc.get(character)

            if encoded is not None and encoded.hex() != hex_code:
                table.noncanon.add(hex_code)
                table.warnings.append(
                    f"código {hex_code} e {encoded.hex()} "
                    f"representam {character!r}; "
                    f"{hex_code} será exibido como tag"
                )

        table.maxlen = max(
            (len(value) for value in table.enc),
            default=1,
        )

        return table

    def to_data(self):
        """
        Serializa o dicionário para dentro do JSON.
        """
        return {
            "pairs": [
                {
                    "h": code,
                    "c": character,
                }
                for code, character in self.dec.items()
            ],
            "warnings": list(self.warnings),
        }

    @classmethod
    def from_data(cls, data, path=None):
        """
        Recria a tabela a partir do dicionário salvo no JSON.
        """
        table = cls()
        table.path = path

        for item in data.get("pairs", []):
            code = item["h"].lower()
            character = item["c"]

            table.dec[code] = character
            table.enc[character] = bytes.fromhex(code)

        for code, character in table.dec.items():
            encoded = table.enc.get(character)

            if encoded is not None and encoded.hex() != code:
                table.noncanon.add(code)

        table.maxlen = max(
            (len(value) for value in table.enc),
            default=1,
        )

        table.warnings = list(data.get("warnings", []))

        return table

    def decode(self, data):
        tokens = []
        index = 0

        while index < len(data):
            found = False

            for length in (2, 1):
                chunk = data[index:index + length]

                if len(chunk) != length:
                    continue

                code = chunk.hex()

                if code in self.dec and code not in self.noncanon:
                    tokens.append(
                        (self.dec[code], chunk, False)
                    )
                    index += length
                    found = True
                    break

                if code in self.dec:
                    tokens.append(
                        (f"<{code}>", chunk, True)
                    )
                    index += length
                    found = True
                    break

            if not found:
                chunk = data[index:index + 1]
                tokens.append(
                    (f"<{chunk.hex()}>", chunk, True)
                )
                index += 1

        output = []

        for token_index, (text, raw, is_tag) in enumerate(tokens):
            if not is_tag:
                window = "".join(
                    item[0]
                    for item in tokens[token_index:token_index + 4]
                )

                for length in range(
                    min(self.maxlen, len(window)),
                    0,
                    -1,
                ):
                    encoded = self.enc.get(
                        window[:length]
                    )

                    if encoded is not None:
                        if (
                            length != len(text)
                            or encoded != raw
                        ):
                            text = f"<{raw.hex()}>"
                        break

            output.append(text)

        return "".join(output)

    def split_text_runs(self, data):
        """
        Divide a entrada em blocos de texto e controle.

        Retorno:

            ("text", texto, bytes)
            ("control", tags, bytes)
        """
        tokens = []
        index = 0

        while index < len(data):
            found = False

            for length in (2, 1):
                chunk = data[index:index + length]

                if len(chunk) != length:
                    continue

                code = chunk.hex()

                if (
                    code in self.dec
                    and code not in self.noncanon
                ):
                    tokens.append(
                        ("text", self.dec[code], chunk)
                    )
                    index += length
                    found = True
                    break

            if found:
                continue

            chunk = data[index:index + 1]
            tokens.append(
                ("control", f"<{chunk.hex()}>", chunk)
            )
            index += 1

        runs = []

        for kind, value, raw in tokens:
            if runs and runs[-1][0] == kind:
                old_kind, old_value, old_raw = runs[-1]
                runs[-1] = (
                    old_kind,
                    old_value + value,
                    old_raw + raw,
                )
            else:
                runs.append((kind, value, raw))

        return runs

    def tokenize(self, text):
        index = 0

        while index < len(text):
            if text[index] == "<":
                match = TAG_RE.match(text, index)

                if match:
                    yield (
                        index,
                        match.end(),
                        bytes.fromhex(match.group(1)),
                    )
                    index = match.end()
                    continue

            found = False

            for length in range(
                min(self.maxlen, len(text) - index),
                0,
                -1,
            ):
                part = text[index:index + length]
                encoded = self.enc.get(part)

                if encoded is not None:
                    yield (
                        index,
                        index + length,
                        encoded,
                    )
                    index += length
                    found = True
                    break

            if not found:
                yield index, index + 1, None
                index += 1

    def encode(self, text):
        output = bytearray()

        for start, end, encoded in self.tokenize(text):
            if encoded is None:
                raise EncodeError(
                    start,
                    text[start:start + 8],
                )

            output += encoded

        return bytes(output)

    def invalid_spans(self, text):
        return [
            (start, end)
            for start, end, encoded in self.tokenize(text)
            if encoded is None
        ]


class Entry:
    __slots__ = (
        "ptrs",
        "orig",
        "tr",
        "note",
        "term",
        "offset",
        "osize",
        "raw",
    )

    def __init__(
        self,
        ptrs,
        orig,
        tr="",
        note="",
        term=True,
        offset=0,
        osize=0,
        raw=b"",
    ):
        self.ptrs = ptrs
        self.orig = orig
        self.tr = tr
        self.note = note
        self.term = term
        self.offset = offset
        self.osize = osize
        self.raw = raw

    @property
    def current(self):
        return self.tr if self.tr != "" else self.orig

    @property
    def has_text(self):
        return bool(TAG_RE.sub("", self.orig).strip())

    def editor_text(self, table):
        """
        Retorna apenas os blocos de texto.
        Blocos de controle são separados por linha em branco.
        """
        if not self.raw:
            return self.orig

        runs = table.split_text_runs(self.raw)

        blocks = [
            value
            for kind, value, raw in runs
            if kind == "text" and value
        ]

        return "\n\n".join(blocks)

    def build_from_editor(self, text, table):
        """
        Recoloca a tradução nos blocos corretos,
        preservando os controles originais.
        """
        if not self.raw:
            return table.encode(text)

        runs = table.split_text_runs(self.raw)

        text_runs = [
            run
            for run in runs
            if run[0] == "text"
        ]

        if not text_runs:
            return self.raw

        translated_parts = text.split("\n\n")

        if len(translated_parts) != len(text_runs):
            raise ValueError(
                f"A entrada possui {len(text_runs)} bloco(s) "
                f"de texto, mas a tradução possui "
                f"{len(translated_parts)} bloco(s). "
                f"Use uma linha em branco entre blocos."
            )

        output = bytearray()
        text_index = 0

        for kind, value, raw in runs:
            if kind == "control":
                output += raw
            else:
                output += table.encode(
                    translated_parts[text_index]
                )
                text_index += 1

        return bytes(output)


class Project:
    def __init__(self):
        self.source = ""
        self.source_path = ""
        self.count = 0
        self.prefix = b""
        self.trailer = b""
        self.entries = []

        self.dictionary_path = ""
        self.dictionary_data = None
        self.language = "English"

    @classmethod
    def from_bin(cls, data, table, source=""):
        if len(data) < 8:
            raise ValueError(
                "Arquivo muito pequeno para ser um xxCstring.bin."
            )

        count, total = struct.unpack_from("<II", data, 0)

        table_start = 8
        text_start = table_start + 4 * count

        if text_start + total > len(data):
            raise ValueError(
                "Cabeçalho inconsistente."
            )

        project = cls()
        project.source = source
        project.count = count

        if count == 0:
            project.trailer = data[text_start + total:]
            return project

        pointers = struct.unpack_from(
            f"<{count}I",
            data,
            table_start,
        )

        text_area = data[
            text_start:text_start + total
        ]

        groups = {}

        for pointer_index, offset in enumerate(pointers):
            if offset >= total:
                raise ValueError(
                    f"Ponteiro {pointer_index} fora da área: "
                    f"{offset:#x}"
                )

            groups.setdefault(offset, []).append(pointer_index)

        offsets = sorted(groups)

        project.prefix = text_area[:offsets[0]]
        project.trailer = data[text_start + total:]

        for position, offset in enumerate(offsets):
            end = (
                offsets[position + 1]
                if position + 1 < len(offsets)
                else total
            )

            payload = text_area[offset:end]
            term = payload.endswith(b"\xff")
            body = payload[:-1] if term else payload

            project.entries.append(
                Entry(
                    groups[offset],
                    table.decode(body),
                    term=term,
                    offset=offset,
                    osize=len(payload),
                    raw=body,
                )
            )

        return project

    def build(self, table):
        text = bytearray(self.prefix)
        pointers = [0] * self.count
        errors = []

        for entry_index, entry in enumerate(self.entries):
            offset = len(text)

            for pointer_index in entry.ptrs:
                pointers[pointer_index] = offset

            try:
                if entry.tr != "":
                    body = entry.build_from_editor(
                        entry.tr,
                        table,
                    )
                elif entry.raw:
                    body = entry.raw
                else:
                    body = table.encode(entry.current)

                text += body

                if entry.term:
                    text += b"\xff"

            except Exception as exc:
                errors.append((entry_index, exc))

        if errors:
            raise BuildError(errors)

        header = struct.pack(
            "<II",
            self.count,
            len(text),
        )

        pointer_table = struct.pack(
            f"<{self.count}I",
            *pointers,
        )

        return (
            header
            + pointer_table
            + bytes(text)
            + self.trailer
        )

    def save(self, path):
        data = {
            "format": 3,
            "source": self.source,
            "source_path": self.source_path,
            "count": self.count,
            "prefix": self.prefix.hex(),
            "trailer": self.trailer.hex(),
            "dictionary_path": self.dictionary_path,
            "dictionary": self.dictionary_data,
            "language": self.language,
            "entries": [],
        }

        for entry in self.entries:
            item = {
                "p": entry.ptrs,
                "o": entry.orig,
                "f": entry.offset,
                "s": entry.osize,
                "r": entry.raw.hex(),
            }

            if entry.tr:
                item["t"] = entry.tr

            if entry.note:
                item["n"] = entry.note

            if not entry.term:
                item["nt"] = 1

            data["entries"].append(item)

        with open(path, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                separators=(",", ":"),
            )

    @classmethod
    def load(cls, path):
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

        project = cls()
        project.source = data.get("source", "")
        project.source_path = data.get("source_path", "")
        project.count = data["count"]
        project.prefix = bytes.fromhex(
            data.get("prefix", "")
        )
        project.trailer = bytes.fromhex(
            data.get("trailer", "")
        )
        project.dictionary_path = data.get(
            "dictionary_path",
            "",
        )
        project.dictionary_data = data.get(
            "dictionary"
        )
        project.language = data.get(
            "language",
            "English",
        )

        for item in data["entries"]:
            raw = bytes.fromhex(
                item.get("r", "")
            )

            project.entries.append(
                Entry(
                    item["p"],
                    item["o"],
                    item.get("t", ""),
                    item.get("n", ""),
                    not item.get("nt"),
                    item.get("f", 0),
                    item.get("s", 0),
                    raw,
                )
            )

        return project

    def export_dump(self, path, only_current=True):
        with open(
            path,
            "w",
            encoding="utf-8",
            newline="\n",
        ) as file:
            for entry in self.entries:
                file.write(
                    ",".join(
                        str(8 + 4 * pointer)
                        for pointer in entry.ptrs
                    )
                    + "\n"
                )

                file.write(
                    (
                        entry.current
                        if only_current
                        else entry.orig
                    )
                    + "\n"
                )

    def import_dump(self, path, fix_u_umlaut=True):
        with open(path, "rb") as file:
            raw = file.read()

        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            text = raw.decode("latin-1")

        lines = text.split("\n")

        if lines and lines[-1] == "":
            lines.pop()

        by_pointer = {
            pointer: entry
            for entry in self.entries
            for pointer in entry.ptrs
        }

        imported = 0
        skipped = 0

        for index in range(0, len(lines) - 1, 2):
            positions = [
                int(value)
                for value in lines[index]
                .replace("\t", "")
                .strip()
                .split(",")
                if value.strip().isdigit()
            ]

            translated = (
                lines[index + 1]
                .replace("\t", "")
                .rstrip("\r")
                .replace(";", "")
            )

            if fix_u_umlaut:
                translated = translated.replace("ü", "ù")

            pointer_index = None

            if positions:
                pointer_index = (positions[0] - 8) // 4

            entry = by_pointer.get(pointer_index)

            if entry is None:
                skipped += 1
                continue

            if (
                translated.strip() != entry.orig.strip()
                and translated.strip()
            ):
                entry.tr = translated
                imported += 1

        return imported, skipped


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print(
            "uso:\n"
            "  python riviera_core.py "
            "Dicionario.txt xxCstring.bin [saida.bin]"
        )
        sys.exit(1)

    table = Table.load(sys.argv[1])

    for warning in table.warnings:
        print("[tabela]", warning)

    with open(sys.argv[2], "rb") as file:
        original = file.read()

    project = Project.from_bin(
        original,
        table,
        sys.argv[2],
    )

    rebuilt = project.build(table)

    print(
        f"{len(project.entries)} entradas; "
        f"round-trip idêntico: {rebuilt == original}"
    )

    if len(sys.argv) > 3:
        with open(sys.argv[3], "wb") as file:
            file.write(rebuilt)