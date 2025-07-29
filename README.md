# GoCardless to Excel

Goes through the steps of the [GoCardless web API](https://bankaccountdata.gocardless.com/companies/complete/developer) to produce a JSON containing the last transactions.
Then uses pandas/openpyxl to parse that json and append it as rows in an existing Excel file (completing missing rows based on Transaction ID column).

## Glossary

* **eIDAS** (Electronic Identification & Trust Services) = EU-wide legislation defining how to certify identity & signatures digitally
* **Providers** = registered organization entrusted to act as a third-party to handle banking information on behalf of users and deliver them granular services
  * **AISP** (Account Information Service Provider) = provider of **AIS**
  * **PISP** (Payment Initiation Service Provider) = provider of **PIS**
* **Requisition** = link to bank account ([sample](https://bankaccountdata.gocardless.com/data))
* **Services** = granular functionality (eg read but not write)
  * **AIS** (Account Information Service) = service to access account balances & transaction histories
  * **PIS** (Payment Initiation Service) = service to initiate/cancel a payments
* **PSD2** (Payment Services Directive 2) = citizen-benefiting EU law mandating banks to offer a secured digital access (API) via third-party apps

## [Developer Quickstart API Steps](https://developer.gocardless.com/bank-account-data/quick-start-guide)

`/!\` Warning: all URLs must end with '/'.

* create a [user secret](https://bankaccountdata.gocardless.com/user-secrets)
* HTTP POST to get access (& refresh) token, save it in a file
* (optional) HTTP GET banks list (Belfius = **BELFIUS_GKCCBEBB**)
* (optional) HTTP POST end user agreement (can change history days)
* HTTP POST to create a requisition (build a link to bank via OAuth)
  * that is similar to <https://bankaccountdata.gocardless.com/data>, but must be done here programmatically
  * set <http://localhost> as return/redirect filler URL
  * response of request contains a _link_ which must be opened in a browser
  * after bank authentication (via ItsMe), browser gets redirected to localhost with a _ref_ parameter (ie requisition ID)
* HTTP GET accounts, passing requisition ID
* HTTP GET transactions, passing account ID
