#!/usr/bin/env python3
"""Audit a controlled PDF ZIP without extracting document text."""
from __future__ import annotations
import argparse, csv, hashlib, json, subprocess, tempfile, zipfile
from pathlib import Path

def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def member_sha256(archive: zipfile.ZipFile, info: zipfile.ZipInfo) -> str:
    digest = hashlib.sha256()
    with archive.open(info) as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def pdf_metadata(archive: zipfile.ZipFile, info: zipfile.ZipInfo) -> dict[str, str]:
    keys = {"Title", "Pages", "PDF version"}
    with tempfile.NamedTemporaryFile(suffix=".pdf") as temporary:
        with archive.open(info) as source:
            for chunk in iter(lambda: source.read(1024 * 1024), b""):
                temporary.write(chunk)
        temporary.flush()
        result = subprocess.run(["pdfinfo", temporary.name], capture_output=True, text=True,
                                encoding="utf-8", errors="replace", check=False)
    values = {"PdfInfoStatus": "OK" if result.returncode == 0 else "FAILED"}
    for line in result.stdout.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            if key.strip() in keys: values[key.strip()] = value.strip()
    return values

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--member-output", required=True, type=Path)
    parser.add_argument("--summary-output", required=True, type=Path)
    args = parser.parse_args()
    with zipfile.ZipFile(args.input) as archive:
        bad_member = archive.testzip(); infos = archive.infolist(); names = [i.filename for i in infos]; rows=[]
        for info in infos:
            is_dir=info.is_dir(); is_pdf=not is_dir and info.filename.lower().endswith('.pdf')
            meta=pdf_metadata(archive, info) if is_pdf else {"PdfInfoStatus":"NOT_APPLICABLE"}
            rows.append({"MemberOrdinal":len(rows)+1,"MemberName":info.filename,"SizeBytes":info.file_size,
                "CompressedSizeBytes":info.compress_size,"CRC32":f"{info.CRC:08x}",
                "SHA256":"" if is_dir else member_sha256(archive,info),"IsDirectory":str(is_dir).lower(),
                "IsPDF":str(is_pdf).lower(),"PdfInfoStatus":meta.get("PdfInfoStatus",""),
                "PDFTitle":meta.get("Title",""),"PDFPages":meta.get("Pages",""),"PDFVersion":meta.get("PDF version","")})
    columns=list(rows[0]) if rows else ["MemberOrdinal","MemberName","SizeBytes","CompressedSizeBytes","CRC32","SHA256","IsDirectory","IsPDF","PdfInfoStatus","PDFTitle","PDFPages","PDFVersion"]
    with args.member_output.open('w',encoding='utf-8',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=columns,lineterminator='\n'); writer.writeheader(); writer.writerows(rows)
    summary={"SourceFilename":args.input.name,"SHA256":file_sha256(args.input),
        "ZipIntegrityStatus":"VERIFIED" if bad_member is None else "CORRUPTED","FirstBadMember":bad_member,
        "TotalMemberCount":len(rows),"PDFMemberCount":sum(r["IsPDF"]=="true" for r in rows),
        "DirectoryMemberCount":sum(r["IsDirectory"]=="true" for r in rows),
        "NonPDFFileCount":sum(r["IsDirectory"]=="false" and r["IsPDF"]=="false" for r in rows),
        "DuplicateMemberNameCount":len(names)-len(set(names)),
        "PDFInfoFailureCount":sum(r["IsPDF"]=="true" and r["PdfInfoStatus"]!="OK" for r in rows)}
    args.summary_output.write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    return 0 if bad_member is None else 2
if __name__ == '__main__': raise SystemExit(main())
