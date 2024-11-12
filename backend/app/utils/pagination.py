"""Utility functions for pagination."""


def get_pagination_info(pagination_object):
    """Utility function to extract pagination information."""
    return {
        "total_items": pagination_object.total,
        "total_pages": pagination_object.pages,
        "current_page": pagination_object.page,
        "next_page": pagination_object.next_num,
        "prev_page": pagination_object.prev_num,
        "per_page": pagination_object.per_page,
    }
