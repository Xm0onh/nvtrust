# Introduction

The attestation verifier tool and SDK are used to verify the
authenticity, integrity, validity, and correctness of attestation
reports generated by GPU operating in Confidential Computing mode. This
document describes the possible error scenarios that may occur when
using the attestation verifier tool and shows the claims and output
messages that can help you recognize such errors. The document also
provides some suggestions on how to handle or avoid these errors.

# Common Error Scenarios

This section outlines the main classes of errors that might happen when
verifying attestation for Confidential Computing workload. Please see
the following sections for a complete list of all possible errors.

-   **Invalid or corrupted attestation report**: These errors occur when
    the attestation report is not well-formed, in unsupported format,
    has missing or incorrect fields, or has been tampered with. The
    verifier tool and SDK will reject such reports and return an error
    code indicating the reason for the failure. To avoid this error, the
    user should ensure that the attestation report is generated by a
    properly configured Nvidia GPU and/or transmitted securely to remote
    services.

-   **Failed RIM Lookup:** These errors happen when RIM lookup cannot
    find a match for a driver version or VBIOS version. This might be
    because Confidential Computing does not support the versions of
    driver and VBIOS being used. Users should check the NVIDIA H100 GPU
    Confidential Computing guide to see the supported versions. If the
    problem still occurs, user should not use the versions that fail and
    report the issue to NVIDIA and the machine owner.

-   **Invalid or corrupted reference integrity measurements (RIM):**
    These errors occur when driver RIM or VBIOS RIM is not available,
    not well-formed, in unsupported format, has missing or incorrect
    fields, or has been tampered with. To avoid this error, the user
    should ensure correct VBIOS, and driver versions are installed in
    the GPU and should ensure RIM is not corrupted/tampered during
    transit.

-   **Expired or invalid certificate**: These errors occur when either
    the certificates in the certificate chain of RIM or device are
    expired or not valid for attestation purposes. Attestation SDK and
    the local verifier tool use X.509 standards to validate the
    certificates and check their validity period and extensions. If a
    RIM for VBIOS or driver has an expired or invalid certificate, user
    should update to a newer version with valid certificates and if a
    device has an expired or invalid certificate, user should find a
    replacement.

-   **Attestation verification error**: This error happens when one or
    more measurements in an attestation report do not match with the
    reference values from driver and VBIOS RIMs. This could be because
    of incorrect settings of the device, altered device, altered
    software, or harmful activity in the device. On encountering this
    error, user must reset their device, reload the driver, and run the
    attestation verification again. If the problem still remains, user
    is advised to stop using the device/software and report to the
    machine owner.

-   **Runtime API errors:** These are errors that happen on the local
    machine when getting attestation reports, certificate chains, or
    basic GPU & Software information. This could be because of a
    software flaw or because of runtime disruptions. User should reboot
    the VM instance and try again. If the problem still remains, user
    should report the error to NVIDIA.

-   **Network or communication error:** This error occurs when the
    verifier tool and SDK encounter a network or communication problem
    when receiving or sending the attestation report or related data.
    The verifier tool and SDK will try to retry or recover from the
    network or communication error, but if the error persists, the
    verifier tool and SDK will abort the verification process and return
    an error code indicating the reason for the failure. To avoid this
    error, the user should ensure that the network and communication
    channels are reliable and stable.

# Full list of errors from CC_Admin tool

The table below displays the various outputs that CC_admin tool can
generate and what causes them. Please note that these outputs are
generated only while using CC_admin tool and not with attestation SDK.
Attestation SDK will only output a claims list as shown in the following
section.

<table>
<colgroup>
<col style="width: 5%" />
<col style="width: 27%" />
<col style="width: 30%" />
<col style="width: 36%" />
</colgroup>
<thead>
<tr class="header">
<th>ID</th>
<th>Error info</th>
<th>Reason for failure</th>
<th>Mitigations</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>1</td>
<td>Attestation report signature verification failed.</td>
<td rowspan="6">The attestation report may be invalid due to corruption,
tampering, or a software bug in the device that generated an incorrect
report.</td>
<td rowspan="6">The user should retrieve the attestation report once
more and run verification. If the problem persists, they should report
the issue to Nvidia.</td>
</tr>
<tr class="even">
<td>2</td>
<td>No GPU runtime measurements found</td>
</tr>
<tr class="odd">
<td>3</td>
<td>Could not parse the GET_MEASUREMENT response message</td>
</tr>
<tr class="even">
<td>4</td>
<td>There are no measurement blocks in the response message</td>
</tr>
<tr class="odd">
<td>5</td>
<td>Measurement block at index " XX" not following DMTF
specification </td>
</tr>
<tr class="even">
<td>6</td>
<td>No certificates found in certificate chain</td>
</tr>
<tr class="odd">
<td>7</td>
<td>The number of certificates fetched from the GPU is unexpected.</td>
<td>The certificate chain must contain 5 certificates, otherwise, it
will in this failure.</td>
<td>The user should attempt to reinstall the current driver or install a
different version, as specified in the NVIDIA H100 GPU Confidential
Computing guide. If the issue persists, the user should report it to
Nvidia.</td>
</tr>
<tr class="even">
<td>8</td>
<td>GPU certificate chain revocation
validation<strong> </strong>failed.</td>
<td>The OCSP validation check for the GPU certificate chain has failed
because one or more certificates in the chain have been revoked.</td>
<td>It is recommended that the user stop the use of the current device
or software and obtain a replacement</td>
</tr>
<tr class="odd">
<td>9</td>
<td>GPU certificate chain validation failed</td>
<td>The signature validation checks for the GPU certificate chain are
not successful.</td>
<td>If the error message indicates that the “verifier_device_root.pem”
file is missing, the user may try to reinstall the attestation SDK. If
the issue persists, the user should try using a different driver
version, as outlined in the NVIDIA H100 GPU Confidential Computing guide
and report the issue to Nvidia if it continues.</td>
</tr>
<tr class="even">
<td>10</td>
<td>Attestation report verification failed</td>
<td rowspan="7"><p>Attestation report verification has failed due to one
of the reasons below:</p>
<ul>
<li><p>Nonce mismatch in GET_MEASUREMENTS</p></li>
<li><p>Driver version mismatch</p></li>
<li><p>VBIOS version mismatch.</p></li>
<li><p>Report retrieval has failed</p></li>
<li><p>GPU certificate chain retrieval has failed</p></li>
<li><p>Extracting individual certificate has failed</p></li>
</ul></td>
<td rowspan="7"><p><strong>Nonce mismatch</strong></p>
<p>The user should attempt to verify the attestation again, using either
the same or a different driver version. If the problem persists, the
user should report the issue to Nvidia.</p>
<p><strong>Driver/VBIOS version mismatch</strong></p>
<p>To confirm these errors, the user can utilize the nvidia-smi utility
to extract the driver/VBIOS versions and cross-check them with the
versions mentioned in the attestation report. The user can try
reinstalling the driver or using different driver versions. If the issue
persists, the user should contact Nvidia for further assistance.</p>
<p><strong>Report/Certificate chain retrieval has failed</strong></p>
<p>Ensure that the system has CC mode enabled and that the Driver is
loaded in persistence mode. To verify that the driver has loaded
successfully, the user can use the nvidia-smi conf-compute –f
command.</p>
<p><strong>Extracting certificates has failed</strong></p>
<p>This issue may arise due to a bug in the driver or corruption during
the retrieval of the certificate chain. It is recommended to try again
with an updated driver version. If the issue persists, the user should
report it to Nvidia for further assistance.</p></td>
</tr>
<tr class="odd">
<td>11</td>
<td>The nonce in the SPDM GET MEASUREMENT request message is not
matching with the generated nonce.</td>
</tr>
<tr class="even">
<td>12</td>
<td>The driver version in attestation report is not matching with the
driver version fetched from the driver</td>
</tr>
<tr class="odd">
<td>13</td>
<td>The vbios version in attestation report is not matching with the
vbios version fetched from the driver</td>
</tr>
<tr class="even">
<td>14</td>
<td>Something went wrong while fetching the attestation report from the
gpu</td>
</tr>
<tr class="odd">
<td>15</td>
<td>Something went wrong while fetching the certificate chains from the
gpu.</td>
</tr>
<tr class="even">
<td>16</td>
<td>Something went wrong while extracting the individual certificates
from the certificate chain.</td>
</tr>
<tr class="odd">
<td>17</td>
<td>Unknown GPU architecture.</td>
<td>The architecture of the detected GPU is not recognized.</td>
<td>To ensure successful confidential computing and attestation, the
user must verify that the GPU connected to the system is compatible and
that the attestation SDK is updated to the latest version.</td>
</tr>
<tr class="even">
<td>18</td>
<td>GPU architecture is not supported.</td>
<td>The architecture of the detected GPU is not supported.</td>
<td>To ensure successful confidential computing and attestation, the
user must verify that the GPU connected to the system is compatible and
that the attestation SDK is updated to the latest version.</td>
</tr>
<tr class="odd">
<td>19</td>
<td>No GPU found</td>
<td>No GPU has been detected in the system.</td>
<td>The user must verify that the GPU is detected on the PCI bus and
that the driver is loaded in persistence mode.</td>
</tr>
<tr class="even">
<td>20</td>
<td>The call to fetch attestation report timed out</td>
<td rowspan="3">Failures due to time out in runtime APIs.</td>
<td rowspan="3">To resolve these issues, the user should verify that the
driver is operating in persistence mode and that the system can
establish a connection with NVIDIA Remote Attestation services.</td>
</tr>
<tr class="odd">
<td>21</td>
<td>The call to fetch GPU Cert chain timed out</td>
</tr>
<tr class="even">
<td>22</td>
<td>The {function_name} call timed out</td>
</tr>
<tr class="odd">
<td>23</td>
<td>Could not fetch the rim file : {rim_id}</td>
<td rowspan="3">The retrieval of Driver or VBIOS RIM was unsuccessful
due to the absence of files or problems with the network.</td>
<td rowspan="3">To address these issues, the user should confirm that a
connection can be established with NVIDIA Remote Attestation services.
Additionally, when using the local verifier tool, the user should ensure
that the correct RIM file path is specified as input.</td>
</tr>
<tr class="even">
<td>24</td>
<td>Could not find the required VBIOS RIM file &lt;path to VBIOS RIM
file&gt;</td>
</tr>
<tr class="odd">
<td>25</td>
<td>Unable to read &lt;path to Driver RIM file&gt;</td>
</tr>
<tr class="even">
<td>26</td>
<td>No Meta element found in the RIM</td>
<td rowspan="11">Failures due to improperly formed or incorrectly
formatted driver or VBIOS RIM.</td>
<td rowspan="11"><p><strong>Steps to try:</strong></p>
<ol type="1">
<li><p>Reinstall the attestation SDK.</p></li>
<li><p>Attempt to retrieve the RIMs again.</p></li>
<li><p>Switch to a new driver version.</p></li>
</ol>
<p>If the issue continues, the user should seek assistance from Nvidia
and the machine owner.</p></td>
</tr>
<tr class="odd">
<td>27</td>
<td>No Signature found in the RIM</td>
</tr>
<tr class="even">
<td>28</td>
<td>No KeyInfor found in the RIM</td>
</tr>
<tr class="odd">
<td>29</td>
<td>X509Data not found in the RIM</td>
</tr>
<tr class="even">
<td>30</td>
<td>X509Certificates not found in the RIM.</td>
</tr>
<tr class="odd">
<td>31</td>
<td>Driver version not found in the RIM</td>
</tr>
<tr class="even">
<td>32</td>
<td>There was a problem while extracting the X509 certificate from the
RIM.</td>
</tr>
<tr class="odd">
<td>33</td>
<td>No golden measurements found in Driver/VBIOS RIM</td>
</tr>
<tr class="even">
<td>34</td>
<td>Schema validation of Driver/VBIOS RIM failed.</td>
</tr>
<tr class="odd">
<td>35</td>
<td>SWID schema file not found</td>
</tr>
<tr class="even">
<td>36</td>
<td>Multiple measurements are assigned to the same index in
{self.rim_name} rim</td>
</tr>
<tr class="odd">
<td>37</td>
<td>RIM signature verification failed</td>
<td rowspan="4">Failures when there are issues with the validation of
the RIM certificate chain</td>
<td rowspan="4"><p>If the error message indicates that the
“verifier_device_root.pem” file is missing, the user may try to
reinstall the attestation SDK.</p>
<p>An OCSP revocation status indicates that the driver or VBIOS is no
longer usable, and the user must switch to an unrevoked version. In the
event of a RIM verification failure, the user must ensure that the
correct, supported versions of the driver and VBIOS are installed. If
the issue persists, the user should report it to Nvidia.</p></td>
</tr>
<tr class="even">
<td>38</td>
<td>Driver/VBIOS RIM cert chain verification failed</td>
</tr>
<tr class="odd">
<td>39</td>
<td>Driver/VBIOS RIM cert chain ocsp status verification failed</td>
</tr>
<tr class="even">
<td>40</td>
<td>Driver/VBIOS RIM verification failed</td>
</tr>
<tr class="odd">
<td>41</td>
<td>The runtime measurements are not matching with the<br />
golden measurements at the following indexes (starting from 0)</td>
<td>There is a mismatch between one or more measurements in the
attestation report and the reference values from the RIMs. This could be
a result of using devtools mode or unsupported versions of the driver or
VBIOS.</td>
<td>The user must ensure that the device is booted in production mode.
If the issue persists in production mode with supported versions, the
user should stop using the system and find a replacement that passes
attestation.</td>
</tr>
<tr class="even">
<td>42</td>
<td>The driver and vbios RIM have measurement at the same index XX</td>
<td>Conflicting measurement indices between the VBIOS and Driver RIMs. A
conflicting index is marked as active in both the driver and VBIOS
RIM.</td>
<td>The user should try using different versions of the driver or VBIOS
and report the issue to Nvidia for further assistance</td>
</tr>
<tr class="odd">
<td>43</td>
<td>Invalid Nonce Size. The nonce should be 32 bytes in length
represented as Hex String</td>
<td rowspan="2">Failures due to invalid nonce size.</td>
<td rowspan="2">The user must ensure that the length of Nonce passed to
Attestation SDK is 32 bytes and retry attestation.</td>
</tr>
<tr class="even">
<td>44</td>
<td>Length of Nonce is greater than max nonce size allowed</td>
</tr>
</tbody>
</table>

# List of claims returned by NVIDIA Remote Verifier

The NVIDIA Remote Attestation Service (NRAS) will return the following
claims, which will have a value of either true or false.

<table>
<colgroup>
<col style="width: 5%" />
<col style="width: 36%" />
<col style="width: 58%" />
</colgroup>
<thead>
<tr class="header">
<th>ID</th>
<th>Claim</th>
<th>Conditions for the Claim to be valid</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>1</td>
<td>x-nvidia-gpu-driver-rim-schema-validated</td>
<td>The Driver RIM has been confirmed to be in accordance with the swid
schema</td>
</tr>
<tr class="even">
<td>2</td>
<td>x-nvidia-gpu-vbios-rim-cert-validated</td>
<td><p>This claim indicates if the following checks completed
successfully for vBIOS RIM.</p>
<ol type="1">
<li><p>Certificate chain is valid.</p></li>
<li><p>Certificate Chain belongs to NVIDIA PKI</p></li>
<li><p>Certificate is not expired</p></li>
<li><p>Certificate is not revoked.</p></li>
</ol></td>
</tr>
<tr class="odd">
<td>3</td>
<td>x-nvidia-gpu-attestation-report-cert-chain-validated</td>
<td><p>This claim indicates if the following checks completed
successfully for Attestation report certificate chain.</p>
<ol type="1">
<li><p>Certificate chain is valid.</p></li>
<li><p>Certificate Chain belongs to NVIDIA PKI</p></li>
<li><p>Certificate is not expired</p></li>
<li><p>Certificate is not revoked.</p></li>
<li><p>FWID of the certificate matches with the Attestation
report</p></li>
</ol></td>
</tr>
<tr class="even">
<td>4</td>
<td>x-nvidia-gpu-driver-rim-schema-fetched</td>
<td>This claim indicates if the verifier can fetch driver RIM from RIM
service.</td>
</tr>
<tr class="odd">
<td>5</td>
<td>x-nvidia-gpu-attestation-report-parsed</td>
<td>This claim indicates if the Attestation Report has been successfully
parsed.</td>
</tr>
<tr class="even">
<td>6</td>
<td>x-nvidia-gpu-nonce-match</td>
<td>The nonce in the Attestation report matches with the initial input
to the GPU while generating the report.</td>
</tr>
<tr class="odd">
<td>7</td>
<td>x-nvidia-gpu-driver-rim-signature-verified</td>
<td><p>For the claim to be valid, the following conditions must be
met:</p>
<ol type="1">
<li><p>The driver RIM schema must be as expected.</p></li>
<li><p>The driver RIM certificate chain must be verified.</p></li>
<li><p>OCSP validation must pass for each certificate in the RIM
certificate chain.</p></li>
<li><p>The driver RIM signature must be verified, and the driver version
must match the version fetched from the GPU information.</p></li>
</ol></td>
</tr>
<tr class="even">
<td>8</td>
<td>x-nvidia-gpu-vbios-rim-signature-verified</td>
<td><p>For the claim to be valid, the following conditions must be
met:</p>
<ol type="1">
<li><p>The VBIOS RIM schema must be as expected.</p></li>
<li><p>The VBIOS RIM certificate chain must be verified.</p></li>
<li><p>OCSP validation must pass for each certificate in the RIM
certificate chain.</p></li>
<li><p>The VBIOS RIM signature must be verified, and the VBIOS version
must match the version fetched from the GPU information.</p></li>
</ol></td>
</tr>
<tr class="odd">
<td>9</td>
<td>x-nvidia-gpu-arch-check</td>
<td>The GPU Architecture in the Attestation report is either AMPERE, or
HOPPER</td>
</tr>
<tr class="even">
<td>10</td>
<td>x-nvidia-attestation-warning</td>
<td>The Attestation warning message is populated when the certificate is
revoked with reason “CERT_HOLD”</td>
</tr>
<tr class="odd">
<td>11</td>
<td>x-nvidia-gpu-measurements-match</td>
<td>The runtime measurements from the Reference Integrity Measurements
(RIM) matches the runtime measurements in the Attestation report.</td>
</tr>
<tr class="even">
<td>12</td>
<td>x-nvidia-gpu-attestation-report-signature-verified</td>
<td>The signature on the Attestation report is verified.</td>
</tr>
<tr class="odd">
<td>13</td>
<td>x-nvidia-gpu-vbios-rim-schema-validated</td>
<td>The vBIOS RIM has been confirmed to be in accordance with the swid
schema</td>
</tr>
<tr class="even">
<td>14</td>
<td>x-nvidia-gpu-driver-rim-cert-validated</td>
<td><p>This claim indicates if the following checks completed
successfully for Driver RIM.</p>
<ol type="1">
<li><p>Certificate chain is valid.</p></li>
<li><p>Certificate Chain belongs to NVIDIA PKI</p></li>
<li><p>Certificate is not expired</p></li>
<li><p>Certificate is not revoked.</p></li>
</ol></td>
</tr>
<tr class="odd">
<td>15</td>
<td>x-nvidia-gpu-vbios-rim-schema-fetched</td>
<td>This field indicates if the verifier can fetch vBIOS RIM from RIM
service.</td>
</tr>
<tr class="even">
<td>16</td>
<td>x-nvidia-gpu-vbios-rim-measurements-available</td>
<td>The VBIOS Reference Integrity Measurement (RIM) and the measurements
within it were successfully interpreted and understood.</td>
</tr>
<tr class="odd">
<td>17</td>
<td>x-nvidia-gpu-driver-rim-driver-measurements-available</td>
<td>The driver Reference Integrity Measurement (RIM) and the
measurements within it were successfully interpreted and
understood.</td>
</tr>
</tbody>
</table>

# NVIDIA Remote Attestation Service – Error codes

Below is a list of all the error codes returned by the Nvidia Remote
Attestation Service (NRAS). In the event of an error, NRAS returns one
of these error codes along with an empty claim.

| CODE | ERROR_MESSAGE                          | DESCRIPTION                                                                             |
|--------|-----------------------------|------------------------------------|
| 4001 | EMPTY_REQUEST                          | Attestation request is empty.                                                           |
| 4002 | INVALID_REQUEST                        | Attestation request is invalid because Attestation report length is less than expected. |
| 4003 | INVALID_NONCE                          | Nonce in the attestation report is either null or of length 0                           |
| 4004 | INVALID_GPU_ARCH                       | GPU architecture in the attestation report is either null or of length 0                |
| 4005 | INVALID_EVIDENCE                       | GPU Evidence is either null or of length 0                                              |
| 4006 | INVALID_EVIDENCE_FORMAT                | Attestation Evidence could not be parsed by NRAS.                                       |
| 4007 | INVALID_CERTIFICATE_CHAIN              | Certificate chain is invalid, and it does not belong to NVIDIA PKI.                     |
| 4008 | INVALID_GOLDEN_MEASUREMENT             | RIM file data could not be parsed by NRAS.                                              |
| 4009 | DRIVER_AND_RIM_MEASUREMENT_SAME_INDEX  | Driver and VBIOS Golden Measurement has measurement at same index                       |
| 4010 | NONCE_NOT_MATCHING                     | Nonce from request is not matching with evidence nonce                                  |
| 4011 | EVIDENCE_CERT_EXPIRED                  | Evidence certificate is expired                                                         |
| 4012 | GPU_ARCHITECTURE_NOT_SUPPORTED         | GPU Architecture is not one of AMPERE or HOPPER                                         |
| 4013 | INVALID_EVIDENCE_SIGNATURE             | Attestation Report Signature is Invalid                                                 |
| 4014 | INVALID_ATTESTATION_CERTIFICATE_CHAIN  | Attestation Certificate chain doesn’t belong to Nvidia PKI                              |
| 4015 | INVALID_RIM_CERTIFICATE_CHAIN          | RIM Certificate chain doesn’t belong to Nvidia PKI                                      |
| 4016 | FWID_NOT_MATCHING                      | FWID from the Attestation Report does not match the FWID in the Device Certificate.     |
| 5000 | INTERNAL_SERVER_ERROR                  | Internal Server Error                                                                   |
| 5001 | ERROR_DURING_OCSP_QUERY                | Error creating OCSP request or communicating with OCSP service.                         |
| 5002 | CERTIFICATE_STATUS_REVOKED             | OCSP Service returned a “REVOKED” status for the certificate                            |
| 5003 | CERTIFICATE_STATUS_UNKNOWN             | OCSP Service returned a “UNKNOWN” status for the certificate                            |
| 5004 | ERROR_VALIDATING_SIGNATURE             | Error during validating evidence signature                                              |
| 5005 | ATTESTATION_TOKEN_FAILURE              | Fail to generate Attestation Token, please retry                                        |
| 5006 | GPU_DRIVER_VERSION_NOT_AVAILABLE       | GPU Driver Version not available in evidence                                            |
| 5007 | GPU_VBIOS_VERSION_NOT_AVAILABLE        | GPU VBIOS Version not available in evidence                                             |
| 5008 | ERROR_DURING_RIM_DOWNLOAD              | NRAS is not able to download RIM file from RIM Service.                                 |
| 5009 | RIM_BUNDLE_NOT_FOUND                   | RIM file is not found in the RIM Service.                                               |
| 5010 | ERROR_PARSING_RIM_CERTIFICATE          | RIM Certificate parsing failed.                                                         |
| 5011 | INVALID_RIM_CERTIFICATE                | RIM Certificate chain is invalid.                                                       |
| 5012 | RIM_NOT_SIGNED                         | RIM is not signed.                                                                      |
| 5013 | INVALID_RIM_SIGNATURE                  | RIM Signature is invalid.                                                               |
| 5014 | FAIL_TO_VALIDATE_RIM_SIGNATURE         | Parsing error when trying to validate RIM Signature.                                    |
| 5015 | ERROR_ATTESTING_EVIDENCE               | Error talking to enclave to Attest the evidence.                                        |
| 5016 | NITRO_ATTESTATION_DOCUMENT_FETCH_ERROR | Fail to download Nitro Attestation Document                                             |

# Reporting an issue to Nvidia

If the remediations above do not help users fix the problems, they can
report their issues at <https://github.com/NVIDIA/nvtrust/issues>.