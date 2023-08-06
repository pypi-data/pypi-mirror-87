# Copyright © 2020 Interplanetary Database Association e.V.,
# BigchainDB and IPDB software contributors.
# SPDX-License-Identifier: (Apache-2.0 AND CC-BY-4.0)
# Code is Apache-2.0 and docs are CC-BY-4.0

from flask import current_app, request
from flask_restful import reqparse, Resource

from bigchaindb.web.views import parameters


class OutputListApi(Resource):
    def get(self):
        """API endpoint to retrieve a list of links to transaction
        outputs.

            Returns:
                A :obj:`list` of :cls:`str` of links to outputs.
        """
        parser = reqparse.RequestParser()
        parser.add_argument('public_key', type=parameters.valid_ed25519,
                            required=True)
        parser.add_argument('spent', type=parameters.valid_bool)
        args = parser.parse_args(strict=True)

        pool = current_app.config['bigchain_pool']
        with pool() as bigchain:
            outputs = bigchain.get_outputs_filtered(args['public_key'],
                                                    args['spent'])
            return [{'transaction_id': output.txid, 'output_index': output.output, 'spent': output.spent}
                    for output in outputs]


    def post(self):
        """API endpoint to retrieve a list of links to transaction
        outputs.

            Returns:
                A :obj:`list` of :cls:`str` of links to outputs.
        """
        
        retValue = []
        requestJson = request.get_json(force=True)

        pubKeys = requestJson['public_keys']

        spent = None

        if "spent" in requestJson:
            spent = requestJson['spent']

        pool = current_app.config['bigchain_pool']
        with pool() as bigchain:

            for pub in pubKeys:
                outputs = bigchain.get_outputs_filtered(pub, spent)
                retValue += [{'transaction_id': output.txid, 'output_index': output.output, 'public_key': pub, 'spent': output.spent if spent is None  else spent }
                        for output in outputs]
        return retValue

        
