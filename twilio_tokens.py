import logging
import os

import streamlit as st
from twilio.rest import Client

logger = logging.getLogger(__name__)


@st.cache_data
def get_ice_servers():
    """Use Twilio's TURN server because Streamlit Community Cloud has changed
    its infrastructure and WebRTC connection cannot be established without TURN server now.  # noqa: E501
    We considered Open Relay Project (https://www.metered.ca/tools/openrelay/) too,
    but it is not stable and hardly works as some people reported like https://github.com/aiortc/aiortc/issues/832#issuecomment-1482420656  # noqa: E501
    See https://github.com/whitphx/streamlit-webrtc/issues/1213
    """

    # Ref: https://www.twilio.com/docs/stun-turn/api
    try:
        account_sid = os.environ["TWILIO_ACCOUNT_SID"]
        auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    except KeyError:
        logger.warning(
            "Twilio credentials are not set. Fallback to a free STUN server from Google."  # noqa: E501
        )
        return [{"urls": ["stun:stun.l.google.com:19302"]}]

    client = Client(account_sid, auth_token)

    token = client.tokens.create()

    return token.ice_servers

                    # {"username": "ecf7567828a9780516808fad84421c900b3df7283330a7a93545168c943c906e",
                    # "ice_servers": [{'url': 'stun:global.stun.twilio.com:3478', 
                    #                  'urls': 'stun:global.stun.twilio.com:3478'}, 
                    #                  {'url': 'turn:global.turn.twilio.com:3478?transport=udp', 
                    #                   'username': 'ecf7567828a9780516808fad84421c900b3df7283330a7a93545168c943c906e', 
                    #                   'urls': 'turn:global.turn.twilio.com:3478?transport=udp', 
                    #                   'credential': 'MzXI3UD8+yGhI1qHCnUsCWLgBJOTCBMLzfow6X6/lig='}, 
                    #                 {'url': 'turn:global.turn.twilio.com:3478?transport=tcp', 
                    #                  'username': 'ecf7567828a9780516808fad84421c900b3df7283330a7a93545168c943c906e', 
                    #                  'urls': 'turn:global.turn.twilio.com:3478?transport=tcp', 
                    #                  'credential': 'MzXI3UD8+yGhI1qHCnUsCWLgBJOTCBMLzfow6X6/lig='}, 
                    #                 {'url': 'turn:global.turn.twilio.com:443?transport=tcp', 
                    #                  'username': 'ecf7567828a9780516808fad84421c900b3df7283330a7a93545168c943c906e', 
                    #                  'urls': 'turn:global.turn.twilio.com:443?transport=tcp', 
                    #                  'credential': 'MzXI3UD8+yGhI1qHCnUsCWLgBJOTCBMLzfow6X6/lig='}],
                    # "date_updated": "2023-11-10 17:47:31+00:00",
                    # "account_sid": "AC049053b997790d028fc79f82a0f5561c",
                    # "ttl": "86400",
                    # "date_created": "2023-11-10 17:47:31+00:00",
                    # "password": "MzXI3UD8+yGhI1qHCnUsCWLgBJOTCBMLzfow6X6/lig="
                    # }