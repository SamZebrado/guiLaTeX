"""Field-level contract for the supported Web conforming roundtrip subset."""

from export_core import (
    export_ir_to_latex,
    import_own_exported_tex_to_ir,
    normalize_web_model_to_ir,
)
from web_prototype.core_to_web_bridge import ir_to_web_model


def test_single_page_ungrouped_web_tex_web_preserves_supported_fields():
    web_ir = {
        "elements": [
            {
                "id": "styled-text",
                "type": "paragraph",
                "content": "保真 roundtrip",
                "page": 1,
                "x": 12,
                "y": 34,
                "width": 156,
                "height": 28,
                "rotation": 17,
                "layer": 9,
                "font_family_zh": "Source Han Sans SC",
                "font_family_en": "Inter",
                "font_size": 15,
                "color": "#123456",
                "alignment": "center",
                "visible": False,
            },
            {
                "id": "front-text",
                "type": "textbox",
                "content": "front",
                "page": 1,
                "x": 20,
                "y": 50,
                "width": 80,
                "height": 20,
                "rotation": 0,
                "layer": 12,
                "font_family_zh": "Noto Sans SC",
                "font_family_en": "Noto Sans",
                "font_size": 16,
                "color": "#abcdef",
                "alignment": "right",
                "visible": True,
            },
        ]
    }

    normalized = normalize_web_model_to_ir(web_ir)
    tex = export_ir_to_latex(normalized)
    imported_ir = import_own_exported_tex_to_ir(tex)
    restored = ir_to_web_model(imported_ir)

    assert normalized == web_ir

    restored_by_id = {element["id"]: element for element in restored["elements"]}
    for original in web_ir["elements"]:
        recovered = restored_by_id[original["id"]]
        assert recovered["page"] == original["page"]
        assert recovered["chineseFont"] == original["font_family_zh"]
        assert recovered["englishFont"] == original["font_family_en"]
        assert recovered["fontSize"] == original["font_size"]
        assert recovered["color"] == original["color"]
        assert recovered["textAlign"] == original["alignment"]
        assert recovered["visible"] == original["visible"]

    # Core's larger layer is front; Web's smaller layerId is front.
    assert restored_by_id["front-text"]["layerId"] < restored_by_id["styled-text"]["layerId"]


def test_web_style_aliases_are_normalized_without_being_overwritten():
    web_model = {
        "elements": [
            {
                "id": "alias-style",
                "type": "textbox",
                "text": "aliases",
                "page": 1,
                "layerId": 3,
                "chineseFont": "Noto Sans SC",
                "englishFont": "Inter",
                "fontSize": 18,
                "color": "#654321",
                "textAlign": "right",
                "visible": False,
            }
        ]
    }

    element = normalize_web_model_to_ir(web_model)["elements"][0]
    assert element["font_family_zh"] == "Noto Sans SC"
    assert element["font_family_en"] == "Inter"
    assert element["font_size"] == 18
    assert element["color"] == "#654321"
    assert element["alignment"] == "right"
    assert element["visible"] is False
