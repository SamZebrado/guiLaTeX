"""Named page contracts in millimetres; unspecified legacy IR remains A4."""

PAGE_DIMENSIONS_MM = {"letter": (215.9, 279.4), "a4": (210, 297)}
WEB_PAGE_FORMAT = "letter"


def resolve_page_contract(ir):
    contract = ir.get("page_contract", {"format": "a4"})
    if not isinstance(contract, dict) or contract.get("format") not in PAGE_DIMENSIONS_MM:
        raise ValueError("Unsupported page_contract: expected format letter or a4")
    page_format = contract["format"]
    width, height = PAGE_DIMENSIONS_MM[page_format]
    return page_format, width, height
