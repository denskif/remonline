#!/usr/bin/env python

import unittest
import webbrowser
import HTMLTestRunner
import os
import glob as G

import src.scaffolds.auth as s_auth
import src.tests.auth as t_auth
import src.tests.orders as t_orders
import src.tests.settings as t_settings
import src.tests.warehouse as t_warehouse
import src.tests.cashflow as t_cashflow
import src.tests.shop as t_shop
import src.tests.refunds as t_refund
import src.tests.invoices as t_invoices
import src.tests.clients as t_client
import src.tests.api as t_api

from src.lib.driver import close_driver


VERBOSE_LEVEL = 2
SUITE = unittest.TestSuite

# Build and run driver
def runner(title=None):
    title = title or 'Regression tests'
    runner = HTMLTestRunner.HTMLTestRunner(
            stream=file('reports/{0}.html'.format(title), 'wb'),
            title=title,
            description='',
        )
    return runner

def load_test(test_case):
    return unittest.TestLoader().loadTestsFromTestCase(test_case)

def run_test(test_suite, suite_title = ''):
    return runner(suite_title).run(test_suite)


REGISTRATION_S = [
    # s_auth.Login,
    t_auth.LoginValidationTests,
    t_auth.LoginToAccountTests,
    t_auth.ValidateRegistrationFormTests,
    t_auth.RegisterPartnerAccountTests,
    t_auth.RegisterNewAccountTests,
]
SETTINGS_S = [
    t_settings.CreateBranchTests,
    t_settings.EditBranchTests,
    t_settings.DeleteBranchTests,
    t_settings.CreateEmployeeTests,
    t_settings.DeleteEmployeeTests,
]
ORDERS_S = [
    t_orders.CreateOrderTests,
    t_orders.EditOrderType,
    t_orders.EditUrgentOrder,
    t_orders.EditInfoAndWorks,
    t_orders.EditDeviceAndMalfunctions,
    t_orders.EditManagerAndTech,
    t_orders.EditOrderAutocomplete,
    t_orders.CreateClientTests,
    t_orders.EditClientTests,
    t_orders.ResetClientTests,
    t_orders.ClientAutomcpleteTests,

    # Order service widget tests
    t_orders.WinboxValidation,
    t_orders.WinboxSrvcInputsValidation,
    t_orders.SrvcAddToBookList,
    t_orders.AddItemsToTableValidation,
    t_orders.AddInOneOrderValidation,
    t_orders.StringActionsValidation,
    t_orders.TooltipsTest,
    t_orders.EditCommentInTableStr,
    t_orders.EditQuontityInTableStr,
    t_orders.EditManualSrvcData,
    t_orders.DiscauntTypeRateTests,
    t_orders.DiscauntTypeCurrencyTests,
    t_orders.FinalDiscauntTypeRateTests,
    t_orders.FinalDiscauntTypeCurrencyTests,
    t_orders.TestForSomeStrWithDiscount,

    # Order finance tests
    t_orders.PrepaymentTests,
    t_orders.CreateOrderPaymentsTests,
    t_orders.DeleteOrderTransaction,
    t_orders.ValidateCalculationOrderPayments,
    t_orders.ClosePaymentDialog,

    t_orders.StatusChangeTests,
    t_orders.StatusClosedFromOrderTests,
    t_orders.StatusClosedFromTableTests,
    t_orders.TimelineComment,
    t_orders.TimelineAddWork,
    t_orders.TimelineAddWorker,
    t_orders.TimelineAddParts,
    t_orders.MassEditChooseOrderTests,
    t_orders.MassEditDeleteOrderTests,
    t_orders.MassEditAssignWorkerTests,
    t_orders.MassEditDialogTests,
    t_orders.CreateOrderAndOneMore,
    t_orders.CreateFromExistingOrder,
    t_orders.CreateFromClosedOrder,
    t_orders.TransferOrderTests,
    t_orders.MassEditTransferOrderTests,
    t_orders.OpenCloseFilterTests,
    t_orders.FilterSimpleInputsTests,
    t_orders.FilterOrderTypeTests,
    t_orders.FilterEngineerTests,
    t_orders.FilterStatusTests,
]
WAREHOUSE_S = [
    t_warehouse.PostingValidationTests,
    t_warehouse.PostingChooseStockValidationTests,
    t_warehouse.CreatePosting,
    t_warehouse.PostingAutocomplete,
    t_warehouse.PostingAddRemoveGoods,
    t_warehouse.DeletePosting,
    t_warehouse.CreateCategory,
    t_warehouse.SubCategory,
    t_warehouse.DeleteCategory,
    t_warehouse.DeleteCategoryWithGood,
    t_warehouse.EditCategory,
    t_warehouse.CreateStock,
    t_warehouse.EditStock,
    t_warehouse.DeleteStock,
    t_warehouse.DeleteLastStock,
    t_warehouse.DeleteStockWithItem,
    t_warehouse.CreateResidue,
    t_warehouse.ValidateResidue,
    t_warehouse.EditResidue,
    t_warehouse.EditCategoryInResidue,
    t_warehouse.EditItemDataInResidue,
    t_warehouse.DeleteResidueFromTable,
    t_warehouse.DeleteResidueFromForm,
    t_warehouse.DeleteResidueHasAmount,
    t_warehouse.CreateWriteOff,
    t_warehouse.ValidateWriteOff,
    t_warehouse.CommentWriteOff,
    t_warehouse.WriteOffAddRemoveGoods,
    t_warehouse.DeleteWriteOff,
    t_warehouse.ValidateBarcode,
    t_warehouse.GenerateBarcode,
    t_warehouse.CreateBarcode,
    t_warehouse.RemoveBarcode,
    t_warehouse.CreatePostingBarcode,
    t_warehouse.FilterTestsForResidueGrid,
    t_warehouse.FilterTestsForBatches,
    t_warehouse.CreateBatchesValidation,
    t_warehouse.MoveSaleBatchesTests,
    t_warehouse.MoveOrderBatchesTests,
    t_warehouse.WriteOffBatchesTests,
    t_warehouse.WarehouseMoveBatchesTests,
]
CASHBOX_S = [
    t_cashflow.ValidateCashbox,
    t_cashflow.CreateCashbox,
    t_cashflow.UpdateCashbox,
    t_cashflow.RemoveCashbox,
    t_cashflow.ValidateIncome,
    t_cashflow.CheckIncomeTransaction,
    t_cashflow.ValidateExpense,
    t_cashflow.CheckExpenseTransaction,
    t_cashflow.ValidateTransfer,
    t_cashflow.MoneyTransfer,
    t_cashflow.RemoveTransaction,
]
SHOP_S = [
    t_shop.ValidateSale,
    t_shop.CreateSale,
    t_shop.CreateDescribedSale,
    t_shop.DeleteSale,
    t_shop.ClosePaymentDialog,
    t_shop.SalePayment,
]
REFUND_S =[
    t_refund.SaleRefund,
    t_refund.ShopRefundPayment,
    t_refund.OrderRefund,
    t_refund.OrderRefundPayment,
    t_refund.RemoveRefund,
]
INVOICE_S = [
    t_invoices.CreateInvoice,
    t_invoices.CreateInvoiceWithData,
    t_invoices.ChangeOfStatus,
    t_invoices.ChangeStatusWithSelectedStatus,
    t_invoices.ChangeInvoiceWithSelectedStatus,
    t_invoices.VisibilityMassEditButton,
    t_invoices.DeleteInvoiceWithMassEdit,
    t_invoices.PrintInvoiceWithMassEdit,
]
CLIENT_S = [
    t_client.ValidateClientTests,
    t_client.CreateClientTests,
    t_client.ClientAttributesTests,
    t_client.RemoveClientTests,
    t_client.MassDeleteClientTests,
    t_client.ClientPhoneNumTests,
    t_client.FilterClientTypesTests,
    t_client.FilterClientKindsTests,
]
API_S = [
    t_api.ApiTokenTests,
    t_api.ApiBranchTests,
    t_api.ApiStuffTests,
    t_api.ApiMarginTests,
    t_api.ApiStatusTests,
    t_api.ApiGetClientsTests,
    t_api.ApiPostFilterClientsTests,
    t_api.ApiBookModelsTests,
    t_api.ApiBookServicesTests,
    t_api.ApiWarehouseTests,
    t_api.ApiGetOrdersTests,
    t_api.ApiPostFilterOrdersTests,
    t_api.ApiFilterClientInOrderTests,
    t_api.ApiChangeClientsTests,
    t_api.ApiChangeOrderStatusTests,
    t_api.ApiFilterOrderIdsTests,
    t_api.ApiFilterOrderTimeAttributes,
]


# Run SELENIUM Test suites
run_test(SUITE(map(load_test, REGISTRATION_S)), "Registration Tests")
run_test(SUITE(map(load_test, SETTINGS_S)), "Settings Tests")
run_test(SUITE(map(load_test, ORDERS_S)), "Orders Tests")
run_test(SUITE(map(load_test, WAREHOUSE_S)), "Warehouse Test")
run_test(SUITE(map(load_test, CASHBOX_S)), "Cashbox Tests")
run_test(SUITE(map(load_test, SHOP_S)), "Shop Tests")
run_test(SUITE(map(load_test, REFUND_S)), "Refunds Tests")
run_test(SUITE(map(load_test, INVOICE_S)), "Invoice Tests")
run_test(SUITE(map(load_test, CLIENT_S)), "Client Tests")

#Run api request tests
run_test(SUITE(map(load_test, API_S)), "API Tests")

close_driver()

for report in G.glob("reports/*.html"):
    webbrowser.open(report)
