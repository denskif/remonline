from discount import ChangeDiscount
from create_order import CreateOrderTests
from close_payment_dialog import ClosePaymentDialog
from update_order import (
    EditOrderType, EditUrgentOrder, EditInfoAndWorks, EditDeviceAndMalfunctions,
    EditManagerAndTech, EditOrderAutocomplete
)
from work import WorkTests, WorkAutocompleteTests, WorkValidationTests
from spare_parts import (
    SpareAddManualyTests, SpareAddFromWarehouseTests, SpareValidationTests
)
from transfer_order import TransferOrderTests
from prepayment import PrepaymentTests
from statuses.status_change import StatusChangeTests
from statuses.status_closed import (
    StatusClosedFromOrderTests, StatusClosedFromTableTests
)
from create_more import (
    CreateOrderAndOneMore, CreateFromExistingOrder, CreateFromClosedOrder
)
from timeline import (
    TimelineComment, TimelineAddWorker, TimelineAddWork, TimelineAddParts,
)
from mass_edit import (
    MassEditChooseOrderTests, MassEditTransferOrderTests,
    MassEditDeleteOrderTests, MassEditAssignWorkerTests, MassEditDialogTests
)

from clients import (
    CreateClientTests, EditClientTests, ResetClientTests, ClientAutomcpleteTests
)

from order_filter.inputs import OpenCloseFilterTests, FilterSimpleInputsTests
from order_filter.order_types import FilterOrderTypeTests
from order_filter.employees import FilterEngineerTests
from order_filter.status import FilterStatusTests

from spare_parts_and_works.add_work_and_parts.winbox_tests import (
    WinboxValidation, WinboxSrvcInputsValidation, SrvcAddToBookList
)
from spare_parts_and_works.add_work_and_parts.edit import (
    EditCommentInTableStr, EditQuontityInTableStr, EditManualSrvcData
)
from spare_parts_and_works.add_work_and_parts.grid import (
    AddItemsToTableValidation, AddInOneOrderValidation, StringActionsValidation,
    TooltipsTest,
)
from spare_parts_and_works.add_work_and_parts.warranty_and_discount import (
    DiscauntTypeRateTests, DiscauntTypeCurrencyTests,
    FinalDiscauntTypeRateTests, FinalDiscauntTypeCurrencyTests,
    TestForSomeStrWithDiscount,
)

from payments.transactions import (
    CreateOrderPaymentsTests, DeleteOrderTransaction,
    ValidateCalculationOrderPayments,
)
