
from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
import logging
from open_webui.constants import ERROR_MESSAGES
from open_webui.env import SRC_LOG_LEVELS
from open_webui.utils.auth import get_admin_user, get_verified_user

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MODELS"])

router = APIRouter()

@router.post("/get", response_model={})
async def get_app_config(user=Depends(get_verified_user)):
    try:
        
        return {
                "application": "bpd_delivery_generation",
                "is_document": True,
                "instructions": "",
                "starter_prompt": ["For Financial Accounting - Account Payable, read the input workshop slides, workshop transcript, user stories, and best practices SAP documentation, then draft a BPD, with the inputs provided", "starter prompt 2", "starter prompt 3", "starter prompt 4"],
                "artifacts": [
                    {
                        "artifact_type": "user_story",
                        "is_mandatory": False,
                        "io": "input"
                    },
                    {
                        "artifact_type": "workshop_slide",
                        "is_mandatory": True,
                        "io": "input"
                    },
                    {
                        "artifact_type": "workshop_transcript",
                        "is_mandatory": True,
                        "io": "input"
                    },
                    {
                        "artifact_type": "output_template",
                        "is_mandatory": True,
                        "io": "output"
                    }
                ]
            }

        # return ChatResponse({"id":12, "title":"jayesh"})
        return ChatResponse(**chat.model_dump())
        
    except Exception as e:
        log.exception(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=ERROR_MESSAGES.DEFAULT()
        )