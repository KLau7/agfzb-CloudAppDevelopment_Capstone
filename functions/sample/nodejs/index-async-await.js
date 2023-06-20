/**
  *
  * main() will be run when you invoke this action
  *
  * @param Cloud Functions actions accept a single parameter, which must be a JSON object.
  *
  * @return The output of this action, which must be a JSON object.
  *
  */
 
/**
 * Get all dealerships
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {
    const state = params.state;
    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({
        authenticator: authenticator
    });
    cloudant.setServiceUrl(params.COUCH_URL);
    try {
        let dbList = await cloudant.postAllDocs({
            db: 'dealerships',
            includeDocs: true,
        });
        let allDocs = dbList.result.rows.map(row => row.doc)
        if (state) allDocs = allDocs.filter(doc => doc.state === state)
        return { body: allDocs };
    } catch (error) {
        return { error: error.description };
    }
}

