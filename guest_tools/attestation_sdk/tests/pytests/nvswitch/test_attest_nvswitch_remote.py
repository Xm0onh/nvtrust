import base64
import json
import os
from unittest import TestCase, mock
from unittest.mock import patch

import pytest
import jwt
import datetime
from nv_attestation_sdk import attestation
from nv_attestation_sdk.attestation import Devices, Environment, Attestation
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from nv_attestation_sdk.nvswitch import attest_nvswitch_remote
import jwt

from nv_attestation_sdk.utils.nras_utils import decode_nras_token
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

overall_claims_file_path = "tests/pytests/data/switch/overall_claims_remote.json"
detached_claims_file_path = "tests/pytests/data/switch/detached_claims_remote.json"

switch_evidence_list = [{"certificate": "test_cert_chain", "evidence": "test_hex_str"}]


class NvSwitchAttestationTestRemote(TestCase):

    def setUp(self):
        private_key = ec.generate_private_key(ec.SECP384R1(), backend=default_backend())

        self.private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        public_key = private_key.public_key()

        subject = issuer = x509.Name(
            [
                x509.NameAttribute(NameOID.COMMON_NAME, "example.com"),
            ]
        )
        self.cert = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(issuer)
            .public_key(public_key)
            .serial_number(x509.random_serial_number())
            .not_valid_before(datetime.datetime.utcnow())
            .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=10))
            .sign(private_key, hashes.SHA256(), default_backend())
        )

    @mock.patch("requests.get")
    @mock.patch("requests.request")
    def test_switch_remote_attest_successful(
        self, nras_mock_request, jwks_mock_request
    ):
        header = {"kid": "nv-eat-kid-test-1234"}
        with open(overall_claims_file_path, "r") as file:
            overall_claims = json.load(file)
            overall_claims_jwt = jwt.encode(
                overall_claims, self.private_pem, algorithm="ES384", headers=header
            )
        encoded_cert = self.cert.public_bytes(serialization.Encoding.DER)
        base64_cert = base64.b64encode(encoded_cert).decode("utf-8")
        with open(detached_claims_file_path, "r") as file:
            detached_claims = json.load(file)
            detached_jwt_token = jwt.encode(
                detached_claims, self.private_pem, algorithm="ES384", headers=header
            )
        nras_mock_response = mock.Mock()
        nras_mock_response.json.return_value = [
            ["JWT", overall_claims_jwt],
            {"SWITCH-0": detached_jwt_token},
        ]
        nras_mock_response.status_code = 200
        nras_mock_request.return_value = nras_mock_response
        jwks_mock_response = mock.Mock()
        jwks_mock_response.json.return_value = {
            "keys": [{"kid": "nv-eat-kid-test-1234", "x5c": [base64_cert]}]
        }
        jwks_mock_request.return_value = jwks_mock_response
        nonce = "931d8dd0add203ac3d8b4fbde75e115278eefcdceac5b87671a748f32364dfcb"
        result, jwt_token = attest_nvswitch_remote.attest(
            nonce, switch_evidence_list, "http://localhost:5000"
        )
        self.assertTrue(result)
        self.assertEqual(jwt_token[0][0], "JWT")
        self.assertEqual(jwt_token[0][1], overall_claims_jwt)
        self.assertEqual(jwt_token[1]["SWITCH-0"], detached_jwt_token)

    @mock.patch("requests.get")
    @mock.patch("requests.request")
    def test_switch_remote_attest_fails_due_to_measurement_mismatch(
        self, nras_mock_request, jwks_mock_request
    ):
        header = {"kid": "nv-eat-kid-test-1234"}
        with open(overall_claims_file_path, "r") as file:
            overall_claims = json.load(file)
            overall_claims["x-nvidia-overall-att-result"] = False
            overall_claims_jwt = jwt.encode(
                overall_claims, self.private_pem, algorithm="ES384", headers=header
            )
        encoded_cert = self.cert.public_bytes(serialization.Encoding.DER)
        base64_cert = base64.b64encode(encoded_cert).decode("utf-8")
        with open(detached_claims_file_path, "r") as file:
            detached_claims = json.load(file)
            detached_claims["measres"] = "fail"
            detached_jwt_token = jwt.encode(
                detached_claims, self.private_pem, algorithm="ES384", headers=header
            )
        nras_mock_response = mock.Mock()
        nras_mock_response.json.return_value = [
            ["JWT", overall_claims_jwt],
            {"SWITCH-0": detached_jwt_token},
        ]
        nras_mock_response.status_code = 200
        nras_mock_request.return_value = nras_mock_response
        jwks_mock_response = mock.Mock()
        jwks_mock_response.json.return_value = {
            "keys": [{"kid": "nv-eat-kid-test-1234", "x5c": [base64_cert]}]
        }
        jwks_mock_request.return_value = jwks_mock_response
        nonce = "931d8dd0add203ac3d8b4fbde75e115278eefcdceac5b87671a748f32364dfcb"
        result, jwt_token = attest_nvswitch_remote.attest(
            nonce, switch_evidence_list, "http://localhost:5000"
        )
        self.assertFalse(result)
        self.assertEqual(jwt_token[0][0], "JWT")
        self.assertEqual(jwt_token[0][1], overall_claims_jwt)

    @patch(
        "nv_attestation_sdk.verifiers.nv_switch_verifier.nvswitch_admin.collect_evidence_remote"
    )
    def test_switch_remote_get_evidence(self, nvswitch_admin):
        ppcie_mode = True
        nvswitch_admin.return_value = switch_evidence_list
        nonce = "931d8dd0add203ac3d8b4fbde75e115278eefcdceac5b87671a748f32364dfcb"
        evidence_list = attest_nvswitch_remote.get_evidence(nonce, ppcie_mode)
        self.assertEqual(len(evidence_list), 1)

    @patch(
        "nv_attestation_sdk.verifiers.nv_switch_verifier.nvswitch_admin.collect_evidence_remote"
    )
    def test_switch_local_get_evidence_fails_due_to_driver_issue(self, nvswitch_admin):
        ppcie_mode = True
        nvswitch_admin.side_effect = Exception("Driver issue encountered")
        nonce = "931d8dd0add203ac3d8b4fbde75e115278eefcdceac5b87671a748f32364dfcb"
        evidence_list = attest_nvswitch_remote.get_evidence(nonce, ppcie_mode)
        self.assertEqual(len(evidence_list), 0)

    def test_build_payload(self):
        evidence_list = {
            "evidence_list": [
                {"certificate": "test_cert_chain", "evidence": "test_hex_str"}
            ]
        }
        payload = attest_nvswitch_remote.build_payload("nonce", evidence_list)
        self.assertEqual(json.loads(payload)["arch"], "LS10")
        self.assertEqual(json.loads(payload)["nonce"], "nonce")

    @mock.patch("requests.get")
    @mock.patch("requests.request")
    def test_switch_remote_attest_fails_when_nras_call_fails(
        self, nras_mock_request, jwks_mock_request
    ):
        header = {"kid": "nv-eat-kid-test-1234"}
        nras_mock_response = mock.Mock()
        nras_mock_response.json.return_value = [
            ["JWT", ""]
        ]
        nras_mock_response.status_code = 500
        nras_mock_request.return_value = nras_mock_response
        nonce = "931d8dd0add203ac3d8b4fbde75e115278eefcdceac5b87671a748f32364dfcb"
        result, jwt_token = attest_nvswitch_remote.attest(
            nonce, switch_evidence_list, "http://localhost:5000"
        )
        self.assertFalse(result)
        self.assertIsNotNone(jwt_token)
    def test_switch_remote_attest_fails_when_creating_request_due_to_serialization_error(
        self
    ):
        class TestClass:
            pass
        result, jwt_token = attest_nvswitch_remote.attest(
            None, TestClass(), "http://localhost:5000"
        )
        self.assertFalse(result)
        self.assertIsNotNone(jwt_token)

    @pytest.fixture(autouse=True)
    def reset(self):
        yield
        Attestation.reset()