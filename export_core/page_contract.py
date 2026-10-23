"""Named page contracts in millimetres; unspecified legacy IR remains A4."""

PAGE_DIMENSIONS_MM = {"letter": (215.9, 279.4), "a4": (210, 297)}
WEB_PAGE_FORMAT = "letter"
# The canonical canvas is 8.5in x 11in. CSS defines 1in as 96 CSS px;
# these are canvas coordinates, independent of display/device pixel ratio.
WEB_CANVAS_INCHES = (8.5, 11)
WEB_CANVAS_PX = tuple(value * 96 for value in WEB_CANVAS_INCHES)
GEOMETRY_FIELDS = ("x", "y", "width", "height")


def web_geometry_to_mm(element):
    width_mm, height_mm = PAGE_DIMENSIONS_MM[WEB_PAGE_FORMAT]
    return {field: element.get(field, 0) * (
        width_mm / WEB_CANVAS_PX[0] if field in ("x", "width")
        else height_mm / WEB_CANVAS_PX[1]
    ) for field in GEOMETRY_FIELDS}


def ir_geometry_to_web_px(element):
    width_mm, height_mm = PAGE_DIMENSIONS_MM[WEB_PAGE_FORMAT]
    return {field: element.get(field, 0) * (
        WEB_CANVAS_PX[0] / width_mm if field in ("x", "width")
        else WEB_CANVAS_PX[1] / height_mm
    ) for field in GEOMETRY_FIELDS}


def resolve_page_contract(ir):
    contract = ir.get("page_contract", {"format": "a4"})
    if not isinstance(contract, dict) or contract.get("format") not in PAGE_DIMENSIONS_MM:
        raise ValueError("Unsupported page_contract: expected format letter or a4")
    page_format = contract["format"]
    width, height = PAGE_DIMENSIONS_MM[page_format]
    return page_format, width, height
