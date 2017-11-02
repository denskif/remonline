from auth import ApiTokenTests

from branch import ApiBranchTests
from employees import ApiStuffTests
from margin import ApiMarginTests
from status import ApiStatusTests

from clients import (
    ApiGetClientsTests, ApiPostFilterClientsTests, ApiChangeClientsTests
)

from orders import (
    ApiGetOrdersTests, ApiPostFilterOrdersTests, ApiChangeOrderStatusTests,
    ApiFilterClientInOrderTests, ApiFilterOrderIdsTests,
    ApiFilterOrderTimeAttributes,
)

from books import ApiBookModelsTests
from books import ApiBookServicesTests

from warehouse import ApiWarehouseTests
