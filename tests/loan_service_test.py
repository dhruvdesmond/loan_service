import datetime
import unittest
import uuid
from unittest.mock import patch, MagicMock
import http

from controller.context_manager import context_user_id, context_actor_user_data
from models.base import GenericResponseModel
from models.loan import LoanInsertModel, LoanModel, RepaymentInsertModel, RepaymentStatus, LoanStatus, AmountInsertModel
from models.user import UserModel, UserTokenData
from service.loan_service import LoanService
from utils.password_hasher import PasswordHasher


class TestLoanService(unittest.TestCase):
    def setUp(self):
        self.loan_insert_data = LoanInsertModel(
            amount=1000.0,
            terms=12,
            status=LoanStatus.PENDING,
            date="2023-07-10"
        )
        self.loan = LoanModel(
            id=1,
            customer_id=1,
            amount=1000.0,
            terms=12,
            status=LoanStatus.PENDING,
            date="2023-07-10",
            repayments=[],
            uuid=uuid.uuid4(),
            created_at=datetime.datetime.now(),
            is_deleted=False
        )
        self.repayment_insert_data = RepaymentInsertModel(
            amount=100.0,
            status=RepaymentStatus.PENDING,
            loan_id=1,
            date="2023-07-10"
        )
        self.amount_insert_data = AmountInsertModel(
            amount=100.0
        )
        self.user = UserModel(
            id=1,
            uuid=uuid.uuid4(),
            created_at="2023-04-09T14:53:10.285Z",
            is_deleted=False,
            first_name="John",
            last_name="Doe",
            email="johndoe@example.com",
            role="customer",
            status="active",
            password_hash=PasswordHasher.get_password_hash("Password123@12")
        )

    @patch("data_adapter.user.User.get_by_uuid")
    @patch("data_adapter.loan.Loan.create_loan")
    @patch("service.loan_service.LoanService.create_repayments")
    def test_create_loan_success(self, mock_create_repayments: MagicMock, mock_create_loan: MagicMock,
                                 mock_get_by_uuid: MagicMock):
        mock_get_by_uuid.return_value = self.user
        mock_create_loan.return_value = self.loan
        mock_create_repayments.return_value = GenericResponseModel(
            status_code=http.HTTPStatus.CREATED,
            message=LoanService.MSG_LOAN_CREATED_SUCCESS,
            data=[]
        )
        context_user_id.set(self.user.uuid)
        context_actor_user_data.set(UserTokenData(
            uuid=str(self.user.uuid),
            role=self.user.role,
            email=self.user.email
        ))
        response = LoanService.create_loan(self.loan_insert_data)
        self.assertEqual(response.status_code, http.HTTPStatus.CREATED)
        self.assertEqual(response.message, LoanService.MSG_LOAN_CREATED_SUCCESS)
        self.assertEqual(response.data, self.loan)

    @patch("data_adapter.loan.Loan.get_by_uuid")
    @patch("data_adapter.loan.Loan.update_loan_by_uuid")
    def test_approve_loan_success(self, mock_update_loan_by_uuid: MagicMock, mock_get_by_uuid: MagicMock):
        mock_get_by_uuid.return_value = self.loan
        response = LoanService.approve_loan("loan_uuid")
        self.assertEqual(response.status_code, http.HTTPStatus.CREATED)
        self.assertEqual(response.message, LoanService.MSG_LOAN_CREATED_SUCCESS)
        self.assertEqual(response.data, self.loan)

    @patch("data_adapter.user.User.get_by_uuid")
    @patch("data_adapter.loan.Loan.get_all_customer_loans")
    def test_get_customer_loans_success(self, mock_get_all_customer_loans: MagicMock, mock_get_by_uuid: MagicMock):
        mock_get_by_uuid.return_value = self.user
        mock_get_all_customer_loans.return_value = [self.loan]
        context_user_id.set(self.user.uuid)
        context_actor_user_data.set(UserTokenData(
            uuid=str(self.user.uuid),
            role=self.user.role,
            email=self.user.email
        ))
        response = LoanService.get_customer_loans()
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(response.message, "Customer loans fetched successfully")
        self.assertEqual(response.data, [self.loan])

    @patch("data_adapter.loan.Loan.get_by_uuid")
    @patch("data_adapter.user.User.get_by_uuid")
    @patch("data_adapter.loan.Repayment.update_repayment_status")
    def test_add_repayment_by_customer_success(self, mock_update_repayment_status: MagicMock,
                                               mock_get_by_uuid: MagicMock, mock_get_by_uuid_2: MagicMock):
        mock_get_by_uuid.return_value = self.user
        mock_get_by_uuid_2.return_value = self.loan
        mock_update_repayment_status.return_value = self.loan
        context_user_id.set(self.user.uuid)
        context_actor_user_data.set(UserTokenData(
            uuid=str(self.user.uuid),
            role=self.user.role,
            email=self.user.email
        ))
        response = LoanService.add_repayment_by_customer(str(self.loan.uuid), str(uuid.uuid4()),
                                                         AmountInsertModel(amount=100.0))
        print(response)
        self.assertEqual(response.status_code, http.HTTPStatus.NOT_FOUND)
