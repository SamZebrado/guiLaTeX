#!/usr/bin/env python3
"""Loopback-only guiLaTeX Web server with thin ExportCore API routes."""

from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
WEB_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from export_core import (  # noqa: E402
    export_ir_to_latex,
    import_own_exported_tex_to_ir,
    normalize_web_model_to_ir,
    validate_tex_profile,
)
from web_prototype.core_to_web_bridge import ir_to_web_model  # noqa: E402


MAX_REQUEST_BYTES = 5 * 1024 * 1024


def export_web_model_to_tex(web_model: dict) -> str:
    if not isinstance(web_model, dict) or not isinstance(web_model.get("elements"), list):
        raise ValueError("请求必须包含 elements 数组")
    normalized = normalize_web_model_to_ir(web_model)
    return export_ir_to_latex(normalized)


def import_conforming_tex_to_web(tex_content: str) -> dict:
    validation = validate_tex_profile(tex_content)
    if not validation["ok"]:
        raise ValueError(validation["message"] + ": " + "; ".join(validation["issues"]))
    return ir_to_web_model(import_own_exported_tex_to_ir(tex_content))


class GuiLatexHandler(SimpleHTTPRequestHandler):
    server_version = "guiLaTeX-Web/1"

    def _read_body(self) -> bytes:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError as error:
            raise ValueError("无效 Content-Length") from error
        if length <= 0:
            raise ValueError("请求正文为空")
        if length > MAX_REQUEST_BYTES:
            raise ValueError("请求超过 5 MB 限制")
        body = self.rfile.read(length)
        if len(body) != length:
            raise ValueError("请求正文不完整")
        return body

    def _send_bytes(self, status: int, body: bytes, content_type: str, filename: str | None = None) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        if filename:
            self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, status: int, payload: dict) -> None:
        self._send_bytes(status, json.dumps(payload, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/api/health":
            self._send_json(200, {"ok": True, "service": "guilatex-web", "core": "ExportCore"})
            return
        super().do_GET()

    def do_POST(self) -> None:  # noqa: N802
        try:
            body = self._read_body()
            if self.path == "/api/export-latex":
                payload = json.loads(body.decode("utf-8"))
                web_model = payload.get("model", payload)
                tex = export_web_model_to_tex(web_model).encode("utf-8")
                self._send_bytes(200, tex, "application/x-tex; charset=utf-8", "guilatex_export.tex")
                return
            if self.path == "/api/import-latex":
                tex_content = body.decode("utf-8")
                self._send_json(200, {"ok": True, "model": import_conforming_tex_to_web(tex_content)})
                return
            self._send_json(404, {"ok": False, "error": "未知 API 路径"})
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError, KeyError, TypeError) as error:
            self._send_json(400, {"ok": False, "error": str(error)})
        except Exception as error:  # Keep local UI failure explicit without exposing a traceback.
            self._send_json(500, {"ok": False, "error": f"ExportCore 处理失败: {error}"})


def main() -> int:
    parser = argparse.ArgumentParser(description="Run guiLaTeX Web with local ExportCore routes")
    parser.add_argument("--host", default="127.0.0.1", help="Bind host (default: loopback only)")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    handler = partial(GuiLatexHandler, directory=str(WEB_ROOT))
    server = ThreadingHTTPServer((args.host, args.port), handler)
    print(f"guiLaTeX Web: http://{args.host}:{args.port}/")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
