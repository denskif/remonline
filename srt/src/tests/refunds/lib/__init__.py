# ~*~ coding: utf-8 ~*~

from src.scaffolds.dialog import open_dialog


REFUND_OPTION_SEL = ".js-refund"
REFUND_DIALOG_SEL = ".b-refund"
REFUND_LABEL_SEL = ".js-refunds-app .b-link"
REFUND_FIRST_ROW_CELL_SEL = ".js-refunds-app .b-table__td"
REFUND_LINK_SEL = ".js-refund-link"
REFUND_ATTRIBUTE = "data-refund-id"


def open_make_refund_dialog(driver):
    return open_dialog(driver, REFUND_OPTION_SEL, REFUND_DIALOG_SEL)

def open_last_refund(driver):
	return open_dialog(driver, REFUND_LABEL_SEL, REFUND_DIALOG_SEL)
