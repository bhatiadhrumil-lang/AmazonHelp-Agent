"""Per-cluster interpretation data for Phase 1C (taxonomy interpretation).

Every cluster 0-202 was audited by reading its 8 representative customer messages
from artifacts/discovery/embeddings/full/embeddings_meta.csv (via the digest
built by scripts/build_cluster_digest.py).

Encoding rules (from the Phase 1C plan):
- preliminary_label is EVIDENCE-BASED, not a final intent name. Families that
  are pure conversation artifacts (acknowledgement / template / closure turns)
  are labelled as such and are NOT intents.
- customer_goal describes what the customer appears to want.
- confidence in the interpretation; coherent (yes/no/uncertain) about whether
  the cluster is one coherent goal.
- possible_parent_intent groups clusters for the preliminary taxonomy.
- merge_candidates / split_candidates record exploratory suggestions.
- "UNCERTAIN" is used where the reps do not support a firm reading.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Family definitions. family_key -> metadata
# label   : preliminary label (evidence based, "Likely ...")
# goal    : customer_goal
# conf    : confidence in reading (high/medium/low)
# coherent: yes / no / uncertain  (is the cluster one coherent goal?)
# parent  : possible_parent_intent (grouping for the preliminary taxonomy)
# kind    : 'intent' | 'artifact' | 'sentiment' | 'contextual' | 'ood'
# ---------------------------------------------------------------------------
FAMILIES = {
    "ack_thanks": {
        "label": "Conversation closure: thank you / acknowledgement",
        "goal": "Acknowledge a reply or close the thread politely; no problem still pending is expressed.",
        "conf": "high", "coherent": "yes", "parent": "Conversation closure (artifact)",
        "kind": "artifact",
    },
    "ack_willdo": {
        "label": "Conversation closure: commitment to follow the suggested action",
        "goal": "Signal that the customer will perform the action suggested by support.",
        "conf": "high", "coherent": "yes", "parent": "Conversation closure (artifact)",
        "kind": "artifact",
    },
    "ack_done": {
        "label": "Conversation closure: reports the requested action is done",
        "goal": "Confirm the requested action (form/link/pickup) has been completed.",
        "conf": "high", "coherent": "yes", "parent": "Conversation closure (artifact)",
        "kind": "artifact",
    },
    "template_affirm": {
        "label": "Conversation closure: short affirmation answers (yes / it is)",
        "goal": "Answer a yes/no check question from support; no separate problem stated.",
        "conf": "medium", "coherent": "yes", "parent": "Conversation closure (artifact)",
        "kind": "artifact",
    },
    "template_neg": {
        "label": "Conversation closure: short negation answers (no / not yet / doesn't say)",
        "goal": "Answer a polarity/data check from support; real problem is only implied by the thread.",
        "conf": "medium", "coherent": "yes", "parent": "Conversation closure (artifact)",
        "kind": "artifact",
    },
    "template_time": {
        "label": "Conversation closure: short time/date answers",
        "goal": "Supply a requested date/time piece of context (when did X happen / what date is shown).",
        "conf": "medium", "coherent": "yes", "parent": "Conversation closure (artifact)",
        "kind": "artifact",
    },
    "empathy_farewell": {
        "label": "Conversation closure: empathy / politeness formula (that's sad, have a nice day)",
        "goal": "React socially to a support remark before closing; no actionable request.",
        "conf": "high", "coherent": "yes", "parent": "Conversation closure (artifact)",
        "kind": "artifact",
    },
    "transitional": {
        "label": "Ambiguous conversational turn (context-dependent, needs the thread)",
        "goal": "UNCERTAIN - reads like a middle-of-thread response; intent only recoverable from surrounding tweets.",
        "conf": "low", "coherent": "uncertain", "parent": "Context-dependent / unclear",
        "kind": "contextual",
    },
    "waiting_status": {
        "label": "Waiting for a response / asking to be answered promptly",
        "goal": "Nudge support to reply; the underlying problem is stated elsewhere in the thread.",
        "conf": "high", "coherent": "yes", "parent": "Support progress: waiting / nudge",
        "kind": "contextual",
    },
    "cs_team_no_response": {
        "label": "Team not responding / still no reply after contacting support",
        "goal": "Get a reply or update from a team that has not answered despite earlier contact.",
        "conf": "high", "coherent": "yes", "parent": "Support progress: waiting / nudge",
        "kind": "intent",
    },
    "resolution_pending": {
        "label": "Awaiting resolution outcome / case progress (investigation, complaint, case)",
        "goal": "Get a concrete resolution or progress update on an open case/complaint/investigation.",
        "conf": "high", "coherent": "yes", "parent": "Support progress: waiting / nudge",
        "kind": "intent",
    },
    "status_update_request": {
        "label": "Asking support to check / verify current status",
        "goal": "Have support look up and confirm the current state of an order/case/account.",
        "conf": "medium", "coherent": "yes", "parent": "Support progress: waiting / nudge",
        "kind": "contextual",
    },
    "negative_frustration": {
        "label": "Frustration / anger with little or no actionable request",
        "goal": "Vent frustration or insult support; a concrete solvable request is absent from the reps.",
        "conf": "high", "coherent": "yes", "parent": "Sentiment / venting (not a customer goal)",
        "kind": "sentiment",
    },
    "fraud_accusation": {
        "label": "Accusation of fraud / scam / cheating",
        "goal": "Assert that Amazon is defrauding the customer; underlying fixable request often absent or generic.",
        "conf": "high", "coherent": "yes", "parent": "Sentiment / venting (not a customer goal)",
        "kind": "sentiment",
    },
    "complaint_service_quality": {
        "label": "Complaint about support quality (copy-paste / bot-like / unhelpful)",
        "goal": "Get real (non-template) help instead of repeated standard replies.",
        "conf": "high", "coherent": "yes", "parent": "Agent / support experience",
        "kind": "intent",
    },
    "agent_escalation": {
        "label": "Escalation to supervisor / manager / senior team",
        "goal": "Have a supervisor or senior team take over the case after frontline support failed.",
        "conf": "high", "coherent": "yes", "parent": "Agent / support experience",
        "kind": "intent",
    },
    "bot_vs_human": {
        "label": "Question whether support is a bot or a human",
        "goal": "Be helped by a human rather than a bot-like response.",
        "conf": "high", "coherent": "yes", "parent": "Agent / support experience",
        "kind": "intent",
    },
    "contact_channel": {
        "label": "How to reach support (phone number / chat option / email)",
        "goal": "Find a working contact channel or a locale-appropriate channel.",
        "conf": "high", "coherent": "yes", "parent": "Contacting support",
        "kind": "intent",
    },
    "contact_phone_issue": {
        "label": "Phone / IVR / callback channel not working",
        "goal": "Report that phone, IVR or callback options fail, and ask for a working alternative.",
        "conf": "high", "coherent": "yes", "parent": "Contacting support",
        "kind": "intent",
    },
    "contact_callback_request": {
        "label": "Asking support to call the customer directly (photo: numbers shared)",
        "goal": "Be contacted by phone because text support is not resolving the issue.",
        "conf": "high", "coherent": "yes", "parent": "Contacting support",
        "kind": "intent",
    },
    "third_party_contact": {
        "label": "How to contact a third party (carrier / seller)",
        "goal": "Understand how to reach a non-Amazon party (carrier, seller, external service).",
        "conf": "high", "coherent": "yes", "parent": "Contacting support",
        "kind": "intent",
    },
    "detail_provided": {
        "label": "Already provided the requested details (DM / form / email / screenshots)",
        "goal": "Stop being asked repeatedly for details already submitted; get the case progressed.",
        "conf": "high", "coherent": "yes", "parent": "Verification / information flow",
        "kind": "contextual",
    },
    "link_issue": {
        "label": "Link / page not working, missing, or not helping",
        "goal": "Get a working link or have the requested action done without a broken form.",
        "conf": "high", "coherent": "yes", "parent": "Verification / information flow",
        "kind": "intent",
    },
    "verify_fax": {
        "label": "Blocked by verification requirements (fax / postal validation)",
        "goal": "Complete identity or address verification through a channel the customer can actually use.",
        "conf": "high", "coherent": "yes", "parent": "Verification / information flow",
        "kind": "intent",
    },
    "phish_email": {
        "label": "Suspicious / phishing email: asking whether it is genuine",
        "goal": "Confirm whether an email received from Amazon is legitimate before acting on it.",
        "conf": "high", "coherent": "yes", "parent": "Security / account safety",
        "kind": "intent",
    },
    "delivery_tracking": {
        "label": "Package / parcel whereabouts (tracking says X but status unclear)",
        "goal": "Find out where a package is and when it will actually arrive.",
        "conf": "high", "coherent": "yes", "parent": "Delivery & shipping",
        "kind": "intent",
    },
    "delivery_delay": {
        "label": "Delivery delayed / expected window passed",
        "goal": "Understand why delivery is late and get a new, reliable arrival time.",
        "conf": "high", "coherent": "yes", "parent": "Delivery & shipping",
        "kind": "intent",
    },
    "delivery_date_change": {
        "label": "Delivery date changed repeatedly",
        "goal": "Stop the promised delivery date from slipping and get the item delivered.",
        "conf": "high", "coherent": "yes", "parent": "Delivery & shipping",
        "kind": "intent",
    },
    "delivery_estimate": {
        "label": "Asking for delivery / dispatch date or estimate window",
        "goal": "Learn the expected or promised delivery/dispatch date.",
        "conf": "medium", "coherent": "yes", "parent": "Delivery & shipping",
        "kind": "intent",
    },
    "delivery_urgency": {
        "label": "Urgent need for delivery today / as a gift",
        "goal": "Get an urgent item delivered in time (today, for a gift, for an event).",
        "conf": "high", "coherent": "yes", "parent": "Delivery & shipping",
        "kind": "intent",
    },
    "delivery_carrier": {
        "label": "Carrier identification or carrier-specific issue",
        "goal": "State which carrier delivered/shipped, or resolve a carrier-specific delivery problem.",
        "conf": "high", "coherent": "yes", "parent": "Delivery & shipping",
        "kind": "intent",
    },
    "carrier_unreachable": {
        "label": "Carrier not reachable / no tracking number returned",
        "goal": "Get a tracking/carrier that is contactable and can actually locate the parcel.",
        "conf": "high", "coherent": "yes", "parent": "Delivery & shipping",
        "kind": "intent",
    },
    "delivery_driver": {
        "label": "Delivery driver behaviour complaint (threw package / did not knock / lied / no contact)",
        "goal": "Report driver behaviour that prevented safe, honest delivery.",
        "conf": "high", "coherent": "yes", "parent": "Delivery & shipping",
        "kind": "intent",
    },
    "misdelivery": {
        "label": "Delivered to wrong address / wrong neighbour / permanently wrong address on file",
        "goal": "Recover a package delivered to the wrong place, or fix the stored address.",
        "conf": "high", "coherent": "yes", "parent": "Delivery & shipping",
        "kind": "intent",
    },
    "package_damaged": {
        "label": "Item arrived damaged / poor packaging",
        "goal": "Resolve damage caused in transit (refund/replacement/compensation).",
        "conf": "high", "coherent": "yes", "parent": "Delivery & shipping",
        "kind": "intent",
    },
    "item_missing": {
        "label": "Item not received although marked delivered / item missing from parcel",
        "goal": "Locate or replace an item that did not arrive despite being marked delivered.",
        "conf": "high", "coherent": "yes", "parent": "Delivery & shipping",
        "kind": "intent",
    },
    "not_dispatched": {
        "label": "Order not yet dispatched / dispatch status",
        "goal": "Find out why an order has not dispatched and get it moving.",
        "conf": "high", "coherent": "yes", "parent": "Delivery & shipping",
        "kind": "intent",
    },
    "shipping_speed": {
        "label": "Paid-for / Prime delivery speed not honoured (one/two-day/same-day)",
        "goal": "Get the delivery speed paid for or promised (Prime), or compensation for the miss.",
        "conf": "high", "coherent": "yes", "parent": "Delivery & shipping",
        "kind": "intent",
    },
    "order_status": {
        "label": "Order status / where is my order (order number supplied)",
        "goal": "Get status or updates for a specific order after repeated requests.",
        "conf": "high", "coherent": "yes", "parent": "Orders & fulfilment",
        "kind": "intent",
    },
    "cancel_order": {
        "label": "Cancel an order / re-order",
        "goal": "Cancel an order and, where possible, re-order correctly.",
        "conf": "high", "coherent": "yes", "parent": "Orders & fulfilment",
        "kind": "intent",
    },
    "refund_request": {
        "label": "Refund / compensation request and refund status",
        "goal": "Obtain a refund or compensation, or confirm the status/arrival of an agreed refund.",
        "conf": "high", "coherent": "yes", "parent": "Orders & fulfilment",
        "kind": "intent",
    },
    "replacement_request": {
        "label": "Replacement request and replacement status",
        "goal": "Obtain a replacement item or confirm the progress of an agreed replacement.",
        "conf": "high", "coherent": "yes", "parent": "Orders & fulfilment",
        "kind": "intent",
    },
    "return_process": {
        "label": "Return / return pickup process issues (scheduling, windows)",
        "goal": "Complete a return: arrange or fix pickup, label, or drop-off.",
        "conf": "high", "coherent": "yes", "parent": "Orders & fulfilment",
        "kind": "intent",
    },
    "charge_inquiry": {
        "label": "Unexpected / repeated / confusing charge (bank statement inconsistency)",
        "goal": "Understand or reverse an unexpected charge and confirm what was paid.",
        "conf": "high", "coherent": "yes", "parent": "Payments & billing",
        "kind": "intent",
    },
    "prime_charge": {
        "label": "Prime / subscription charge or trial confusion",
        "goal": "Understand why a Prime/trial charge occurred and cancel or reverse it.",
        "conf": "high", "coherent": "yes", "parent": "Payments & billing",
        "kind": "intent",
    },
    "payment_method": {
        "label": "Payment method declined / card payment failures",
        "goal": "Complete a purchase when the card or payment method keeps failing.",
        "conf": "high", "coherent": "yes", "parent": "Payments & billing",
        "kind": "intent",
    },
    "gift_card": {
        "label": "Gift card balance / redemption / locked card",
        "goal": "Use, recover, or redeem a gift card (balance, code, locked balance).",
        "conf": "high", "coherent": "yes", "parent": "Payments & billing",
        "kind": "intent",
    },
    "account_login": {
        "label": "Account login / access problems",
        "goal": "Restore access to an account (login, password, locked or duplicate account).",
        "conf": "high", "coherent": "yes", "parent": "Account & settings",
        "kind": "intent",
    },
    "price_change": {
        "label": "Price changed vs listing / sale price discrepancy",
        "goal": "Understand or adjust a price that changed after listing, in cart, or at checkout.",
        "conf": "high", "coherent": "yes", "parent": "Shopping & catalogue",
        "kind": "intent",
    },
    "stock_availability": {
        "label": "Stock / CODPIN / pincode availability; item out of stock",
        "goal": "Find out why an item cannot be ordered or fulfilled to the customer's location.",
        "conf": "high", "coherent": "yes", "parent": "Shopping & catalogue",
        "kind": "intent",
    },
    "seller_issue": {
        "label": "Third-party seller fulfilment / feedback / communication issues",
        "goal": "Resolve an order handled by an external (third-party) seller or its carrier.",
        "conf": "high", "coherent": "yes", "parent": "Marketplace & sellers",
        "kind": "intent",
    },
    "region_mismatch": {
        "label": "Region / marketplace mismatch (UK / US / DE link or availability)",
        "goal": "Get the correct marketplace/link for the customer's country or clarify regional availability.",
        "conf": "medium", "coherent": "yes", "parent": "Shopping & catalogue",
        "kind": "intent",
    },
    "promo_code": {
        "label": "Promo or verification code not received / redemption failure",
        "goal": "Receive or redeem a code (promo, gift, verification).",
        "conf": "medium", "coherent": "yes", "parent": "Promotions & offers",
        "kind": "intent",
    },
    "contest_promo": {
        "label": "Contest / quiz participation and results",
        "goal": "Get contest results, verify participation, or resolve a quiz/contest issue.",
        "conf": "high", "coherent": "yes", "parent": "Promotions & offers",
        "kind": "intent",
    },
    "product_question": {
        "label": "Product specification / eligibility question before purchase",
        "goal": "Get accurate information about a product (specs, battery, compatibility) before buying.",
        "conf": "high", "coherent": "yes", "parent": "Products & defects",
        "kind": "intent",
    },
    "product_defect": {
        "label": "Defective / broken / failing product (incl. warranty)",
        "goal": "Get a defective product fixed, replaced or refunded (incl. warranty claims).",
        "conf": "high", "coherent": "yes", "parent": "Products & defects",
        "kind": "intent",
    },
    "preorder": {
        "label": "Pre-order release date issues (games, consoles, media)",
        "goal": "Get clarity on pre-order release date/delivery or the associated bonus/edition.",
        "conf": "high", "coherent": "yes", "parent": "Products & defects",
        "kind": "intent",
    },
    "device_issue": {
        "label": "Device or app not working (generic troubleshooting)",
        "goal": "Get a device/app working again after suggested fixes failed.",
        "conf": "high", "coherent": "yes", "parent": "Amazon devices & apps",
        "kind": "intent",
    },
    "fire_tv": {
        "label": "Fire TV Stick issues (control, storage, freezing)",
        "goal": "Fix Fire TV Stick behaviour (volume, storage, freezing, Miracast).",
        "conf": "high", "coherent": "yes", "parent": "Amazon devices & apps",
        "kind": "intent",
    },
    "echo_alexa": {
        "label": "Echo / Alexa device issues and routines",
        "goal": "Fix Echo/Alexa behaviour (routines, music, multi-device control) or understand device features.",
        "conf": "high", "coherent": "yes", "parent": "Amazon devices & apps",
        "kind": "intent",
    },
    "kindle_app": {
        "label": "Kindle app issues (crashes, sync, content access)",
        "goal": "Fix Kindle application behaviour (open/crash/sync).",
        "conf": "high", "coherent": "yes", "parent": "Amazon devices & apps",
        "kind": "intent",
    },
    "connectivity": {
        "label": "Network / router / connectivity issues affecting a service",
        "goal": "Diagnose a connectivity problem blocking an Amazon service.",
        "conf": "high", "coherent": "yes", "parent": "Amazon devices & apps",
        "kind": "intent",
    },
    "prime_video": {
        "label": "Prime Video: streaming / catalogue / subtitles / regional availability",
        "goal": "Fix streaming/playback problems, missing subtitles, or explain/change catalogue availability.",
        "conf": "high", "coherent": "yes", "parent": "Digital content & streaming",
        "kind": "intent",
    },
    "music": {
        "label": "Music Unlimited availability / playback issues",
        "goal": "Fix Amazon Music playback or availability for specific tracks.",
        "conf": "high", "coherent": "yes", "parent": "Digital content & streaming",
        "kind": "intent",
    },
    "review_q": {
        "label": "Product review removed / review guideline question",
        "goal": "Understand why a review was removed or get it restored.",
        "conf": "high", "coherent": "yes", "parent": "Community & reviews",
        "kind": "intent",
    },
    "off_topic_chat": {
        "label": "Off-topic / social chatter (out-of-domain for a support triage)",
        "goal": "UNCERTAIN - casual/emotional conversation not expressing a support request.",
        "conf": "medium", "coherent": "uncertain", "parent": "Out-of-domain / conversational",
        "kind": "ood",
    },
    "resolution_thanks": {
        "label": "Issue now resolved / sorted - acknowledgment",
        "goal": "Confirm the problem is resolved and close the thread; no further action requested.",
        "conf": "high", "coherent": "yes", "parent": "Conversation closure (artifact)",
        "kind": "artifact",
    },
    "next_step_guidance": {
        "label": "Asking what to do next / for guidance",
        "goal": "Get clear next steps or guidance for the current situation.",
        "conf": "medium", "coherent": "yes", "parent": "Support progress: waiting / nudge",
        "kind": "intent",
    },
    "false_advertising": {
        "label": "Claims of false / misleading advertising",
        "goal": "Protest against advertised claims (delivery time, price, listing) that were not honoured.",
        "conf": "medium", "coherent": "yes", "parent": "Complaints & sentiment",
        "kind": "sentiment",
    },
    "gift_delivery": {
        "label": "Gift / holiday delivery issues (timing, damaged gift)",
        "goal": "UNCERTAIN - gift-related delivery complaints around Christmas; mixes timing and damage themes.",
        "conf": "medium", "coherent": "uncertain", "parent": "Delivery & shipping",
        "kind": "intent",
    },
    "shipping_cost": {
        "label": "Shipping cost / free-shipping threshold question",
        "goal": "Understand shipping costs or the free-shipping/eligibility threshold.",
        "conf": "medium", "coherent": "yes", "parent": "Shopping & catalogue",
        "kind": "intent",
    },
    "time_estimate_query": {
        "label": "Asking how long / how soon (time estimate)",
        "goal": "Get a time estimate for a pending action (resolution, delivery, follow-up).",
        "conf": "medium", "coherent": "yes", "parent": "Support progress: waiting / nudge",
        "kind": "contextual",
    },
    "megacluster_unclear": {
        "label": "Large mixed cluster - not one coherent intent (needs sub-splitting)",
        "goal": "UNCERTAIN - multiple goals appear to be mixed (delivery/order/marketplace), incl. multilingual.",
        "conf": "low", "coherent": "no", "parent": "Needs re-clustering",
        "kind": "contextual",
    },
}

# ---------------------------------------------------------------------------
# Per-cluster family assignment. Optional overrides per cluster:
#   overrides = {cluster_id: (family_key, {field: value, ...})}
# ---------------------------------------------------------------------------
CLUSTERS: dict[int, tuple[str, dict]] = {}

def _set(spec: dict[int, str]) -> None:
    for cid, family in spec.items():
        CLUSTERS[cid] = (family, {})

# --- conversation closure / artifact families ---
_set({0: "ack_thanks", 1: "ack_thanks", 2: "ack_thanks", 3: "ack_thanks",
      4: "ack_thanks", 5: "ack_thanks", 6: "ack_thanks", 17: "ack_thanks",
      25: "ack_thanks", 45: "ack_thanks", 52: "ack_thanks", 76: "ack_thanks",
      107: "ack_thanks", 127: "ack_thanks", 128: "ack_thanks", 130: "ack_thanks",
      131: "ack_thanks", 132: "ack_thanks", 133: "ack_thanks", 134: "ack_thanks",
      126: "empathy_farewell", 118: "empathy_farewell"})
_set({72: "ack_willdo", 85: "ack_done", 87: "ack_done", 110: "ack_willdo",
      111: "ack_willdo", 112: "ack_willdo", 113: "ack_willdo", 121: "ack_willdo",
      123: "ack_done"})
_set({114: "template_neg", 115: "template_neg", 116: "template_neg",
      117: "template_neg", 124: "template_affirm", 125: "template_affirm",
      167: "template_time", 175: "template_time"})

# --- waiting / nudge / no response ---
_set({158: "waiting_status", 159: "waiting_status", 75: "cs_team_no_response",
      185: "cs_team_no_response", 29: "cs_team_no_response",
      26: "status_update_request", 41: "status_update_request"})
_set({30: "resolution_pending", 43: "resolution_pending", 61: "resolution_pending",
      64: "resolution_pending", 140: "resolution_pending"})

# --- sentiment / venting ---
_set({9: "negative_frustration", 49: "negative_frustration", 83: "negative_frustration",
      135: "negative_frustration", 138: "fraud_accusation"})
# 32/108/42/70/122 are entangled; handled individually below with overrides.

# --- agent / support experience ---
_set({119: "complaint_service_quality", 139: "complaint_service_quality",
      88: "complaint_service_quality", 95: "complaint_service_quality",
      79: "complaint_service_quality", 141: "agent_escalation",
      142: "agent_escalation", 129: "agent_escalation", 19: "bot_vs_human"})

# --- contact support ---
_set({36: "contact_channel", 163: "contact_channel", 160: "contact_phone_issue",
      164: "contact_phone_issue", 157: "contact_callback_request",
      161: "third_party_contact"})

# --- verification / information flow ---
_set({11: "detail_provided", 14: "detail_provided", 50: "detail_provided",
      51: "detail_provided", 57: "detail_provided", 58: "detail_provided",
      59: "detail_provided", 60: "detail_provided", 73: "detail_provided",
      74: "detail_provided", 78: "detail_provided", 136: "detail_provided",
      178: "detail_provided", 190: "detail_provided", 191: "detail_provided",
      53: "link_issue", 54: "link_issue", 55: "link_issue", 56: "link_issue",
      162: "verify_fax", 152: "phish_email"})

# --- delivery & shipping ---
_set({146: "delivery_tracking", 186: "delivery_tracking", 196: "delivery_tracking",
      195: "delivery_tracking", 192: "delivery_delay", 172: "delivery_delay",
      48: "delivery_delay", 174: "delivery_delay", 176: "delivery_delay",
      193: "delivery_date_change", 166: "delivery_estimate", 47: "delivery_estimate",
      165: "delivery_urgency", 153: "not_dispatched",
      10: "delivery_carrier", 147: "delivery_carrier", 148: "delivery_carrier",
      149: "delivery_carrier", 150: "delivery_carrier", 18: "delivery_carrier",
      16: "delivery_carrier", 20: "delivery_carrier", 24: "delivery_carrier",
      177: "carrier_unreachable", 151: "carrier_unreachable",
      137: "delivery_driver", 198: "delivery_driver",
      197: "misdelivery", 106: "misdelivery",
      144: "package_damaged", 15: "item_missing", 66: "item_missing",
      86: "item_missing", 62: "shipping_speed", 155: "shipping_speed",
      194: "shipping_speed", 156: "shipping_speed"})

# --- orders & fulfilment ---
_set({71: "order_status", 201: "order_status", 202: "order_status",
      183: "refund_request", 189: "refund_request",
      187: "replacement_request", 188: "return_process", 46: "return_process",
      200: "cancel_order", 199: "cancel_order", 145: "product_defect",
      34: "ack_thanks"})

# --- payments & billing ---
_set({179: "charge_inquiry", 180: "prime_charge", 154: "prime_charge",
      181: "payment_method", 182: "gift_card"})

# --- account ---
_set({184: "account_login"})


def _setmany(spec: dict[int, str]) -> None:
    for cid, family in spec.items():
        CLUSTERS[cid] = (family, {})

# --- shopping / catalogue / marketplace ---
_setmany({12: "contest_promo", 108: "contest_promo", 13: "stock_availability",
          23: "stock_availability", 32: "negative_frustration",
          33: "region_mismatch", 44: "region_mismatch",
          8: "price_change", 171: "price_change",
          169: "seller_issue", 168: "seller_issue", 28: "seller_issue",
          23: "stock_availability", 31: "delivery_delay"})

# --- product / devices / content ---
_setmany({77: "product_question", 80: "product_question", 90: "product_defect",
          104: "product_defect", 38: "product_defect", 145: "product_defect",
          120: "preorder", 39: "preorder", 40: "preorder",
          94: "fire_tv", 68: "echo_alexa", 69: "echo_alexa",
          102: "kindle_app", 101: "device_issue", 97: "device_issue",
          98: "device_issue", 103: "connectivity",
          82: "prime_video", 81: "prime_video", 96: "prime_video",
          99: "prime_video", 100: "prime_video", 105: "prime_video",
          67: "music", 27: "review_q",
          122: "off_topic_chat", 109: "off_topic_chat"})

# --- context-dependent / unclear / OOD ---
CLUSTERS[34] = ("ack_thanks", {"label": "Item has arrived (resolution acknowledgment)",
    "goal": "Confirm the package/item has now arrived; closing the thread."})
CLUSTERS[37] = ("complaint_service_quality", {"coherent": "uncertain", "conf": "medium",
    "label": "Regional (ES/FR) delivery & support quality complaints",
    "goal": "UNCERTAIN - Spanish/French-locale texts mixing delivery complaints and support-quality complaints."})
CLUSTERS[143] = ("gift_delivery", {"coherent": "uncertain", "conf": "medium",
    "label": "Gift delivery around Christmas (DE/FR comments on timing/damage)",
    "goal": "UNCERTAIN - gift-related delivery timing complaints around the holidays."})
CLUSTERS[92] = ("template_affirm", {"coherent": "uncertain",
    "label": "Short affirmative answers (action done but problem persists)",
    "goal": "Confirm an action was done while signalling the problem continues."})
CLUSTERS[22] = ("resolution_thanks", {})
CLUSTERS[65] = ("resolution_thanks", {})
CLUSTERS[89] = ("resolution_thanks", {})
CLUSTERS[21] = ("promo_code", {})
CLUSTERS[35] = ("link_issue", {"label": "Ticket / contact form limitations (closed, no reply option)",
    "goal": "Work around a closed ticket or contact form that blocks further replies."})
CLUSTERS[63] = ("next_step_guidance", {})
CLUSTERS[84] = ("false_advertising", {})
CLUSTERS[91] = ("template_affirm", {})
CLUSTERS[93] = ("template_affirm", {})
CLUSTERS[170] = ("shipping_cost", {})
CLUSTERS[173] = ("time_estimate_query", {})
CLUSTERS[7] = ("megacluster_unclear", {})
CLUSTERS[42] = ("transitional", {"coherent": "uncertain", "conf": "low",
    "label": "Ambiguous thread follow-up (re.: what was already said / done)",
    "goal": "Continue or clarify an earlier statement in the thread; intent needs surrounding context."})
CLUSTERS[70] = ("off_topic_chat", {"coherent": "uncertain", "conf": "low",
    "label": "Social / @-mention chatter (ambiguous, multilingual)",
    "goal": "UNCERTAIN - @-mention reaction or idle chatter rather than a solvable request."})
CLUSTERS[108] = ("contest_promo", {"coherent": "uncertain", "conf": "medium",
    "label": "Hinglish queries mixing contest results and refund expectations",
    "goal": "UNCERTAIN - appears to combine contest-result and refund queries in Hindi/Hinglish."})
CLUSTERS[32] = ("negative_frustration", {"coherent": "uncertain", "conf": "medium",
    "label": "India-market frustration / availability feedback (mixed)",
    "goal": "UNCERTAIN - complains about India support/promises and asks to bring products to India."})
CLUSTERS[31] = ("delivery_delay", {"label": "Delivery failing around Diwali / festivals (India)",
    "goal": "Get the promised festive-season delivery honoured or the failed item sorted."})
CLUSTERS[145] = ("product_defect", {"label": "Phone (mobile) item issues: replacement / delivery of a phone",
    "goal": "Sort a phone order that involves replacement, return or delivery problems."})

# ---------------------------------------------------------------------------
# Merge candidate groups (TASK 4) - exploratory, for human validation.
# ---------------------------------------------------------------------------
MERGE_GROUPS = [
    {"group_id": "MG-01", "member_clusters": [0, 1, 2, 3, 4, 5, 6, 17, 45, 52, 76, 107, 127, 128, 130, 131, 132, 133, 134],
     "rationale": "All are short thank-you / acknowledgement turns (high exact-dup share); none carries its own problem.",
     "evidence": "exact_dup_share 0.93-1.0 in clusters 0-6; reps read as pure thanks.",
     "candidate_label": "Conversation closure: thank you",
     "confidence": "high"},
    {"group_id": "MG-02", "member_clusters": [72, 85, 87, 110, 111, 112, 113, 121],
     "rationale": "All commit to do the suggested action ('will do', 'done', 'I'll try').",
     "evidence": "reps show 'will do', 'done', 'I'll try that'.",
     "candidate_label": "Conversation closure: commitment / action done",
     "confidence": "high"},
    {"group_id": "MG-03", "member_clusters": [114, 115, 116, 117, 124, 125, 167, 175],
     "rationale": "One-word/short polarity, date or status answers to support checks.",
     "evidence": "reps like 'no it isn't', 'yes it is', 'December 1', 'Yesterday'.",
     "candidate_label": "Conversation closure: short answer turns",
     "confidence": "medium"},
    {"group_id": "MG-04", "member_clusters": [158, 159],
     "rationale": "Both are 'still waiting for a reply' nudges.",
     "evidence": "reps 'Still waiting for reply', 'Still waiting...'.",
     "candidate_label": "Waiting for support response (nudge)",
     "confidence": "high"},
    {"group_id": "MG-05", "member_clusters": [29, 75, 185],
     "rationale": "No reply from team despite earlier contact (some re emails).",
     "evidence": "reps 'Didn't get any response from your team', 'still no response', 'no mail received'.",
     "candidate_label": "No response from team / still no update",
     "confidence": "high"},
    {"group_id": "MG-06", "member_clusters": [11, 14, 50, 51, 57, 58, 60, 73, 74, 78, 136, 178, 190, 191],
     "rationale": "Customer states details were already shared (DM / form / email / screenshots).",
     "evidence": "reps 'Just sent you a dm', 'I have filled the form', 'Already Shared The Details', 'Email sent.'.",
     "candidate_label": "Details already provided / stop re-asking",
     "confidence": "high"},
    {"group_id": "MG-07", "member_clusters": [53, 54, 55, 56],
     "rationale": "Link/page problem: broken, blank, not helpful, or link not received.",
     "evidence": "reps 'blank page', 'Where is the link?', 'none of link provided is working'.",
     "candidate_label": "Link / page not working or missing",
     "confidence": "high"},
    {"group_id": "MG-08", "member_clusters": [10, 147, 148, 149, 150],
     "rationale": "Carrier-identification short answers ('carrier: AMZL US', 'It was USPS', 'UPS').",
     "evidence": "high exact-dup, reps of the form '<carrier>'.",
     "candidate_label": "Carrier identification (AMZL / UPS / USPS)",
     "confidence": "high"},
    {"group_id": "MG-09", "member_clusters": [26, 30, 41, 140],
     "rationale": "Asking for a status / update / check on the case.",
     "evidence": "reps 'What's the update', 'Any Progress regarding my complaint', 'Now check it'.",
     "candidate_label": "Requesting status / update on open case",
     "confidence": "medium"},
]

# ---------------------------------------------------------------------------
# Split candidate clusters (TASK 5) - exploratory, for human validation.
# ---------------------------------------------------------------------------
SPLIT_CANDIDATES = [
    {"cluster_id": 7, "size_hint": 12267,
     "split_rationale": "Heterogeneous multilingual megacluster; reps mix delivery, returns, seller app and contract disputes.",
     "evidence": "reps in es/de/fr/en touch different goals ('SAV Amazon', returns page, seller app, paid-for deck).",
     "sub_themes_observed": "delivery status; returns; third-party marketplace; Prime/contract; language groups",
     "confidence": "high"},
    {"cluster_id": 59, "size_hint": 1097,
     "split_rationale": "Cluster formed mainly because members attach URL/screenshots; underlying problem varies.",
     "evidence": "url_share=0.99; text short, real issue only visible in attached content.",
     "sub_themes_observed": "order status; delivered-not-received; generic 'this is what I see'",
     "confidence": "medium"},
    {"cluster_id": 42, "size_hint": 648,
     "split_rationale": "Transitional thread turn, multiple distinct sub-conversations.",
     "evidence": "reps reference 'talked to customer service', 'deleted tweet', 'missed your tweet', 'tata docomo'.",
     "sub_themes_observed": "channel switching; correcting earlier tweet; chronology confusion",
     "confidence": "medium"},
    {"cluster_id": 122, "size_hint": 580,
     "split_rationale": "Casual emoji-driven chatter in several languages; some contain a faint request.",
     "evidence": "emoji-heavy reps ('Ya estoy super complicado? no, loving it', 'Mãos dadas').",
     "sub_themes_observed": "pure chatter; goodwill-plea; multilingual",
     "confidence": "medium"},
    {"cluster_id": 156, "size_hint": 1967,
     "split_rationale": "Prime-related texts that mix complaints: membership benefit, delivery promise, credit/compensation.",
     "evidence": "reps mention 'prime benefits', 'Prime extended', 'packages not delivered', 'previous Prime acc credit'.",
     "sub_themes_observed": "prime charge/benefit; prime delivery miss; compensation credit",
     "confidence": "medium"},
    {"cluster_id": 139, "size_hint": 1521,
     "split_rationale": "Support-quality complaint cluster; root problems behind the anger are various.",
     "evidence": "reps cover disconnected calls, useless weblink form, escalation management, 140-char limits.",
     "sub_themes_observed": "escalation; invalid response; contact-channel failures",
     "confidence": "low"},
    {"cluster_id": 184, "size_hint": 1044,
     "split_rationale": "Largest account cluster - login vs locked vs duplicate vs activation may deserve a split.",
     "evidence": "reps 'not able to login', 'id already exists', 'account is unlocked BUT ITS NOT'.",
     "sub_themes_observed": "login failure; duplicate account; locked account; activation",
     "confidence": "low"},
    {"cluster_id": 143, "size_hint": 261,
     "split_rationale": "Holiday/gift delivery texts also mention damaged/returned gifts.",
     "evidence": "reps 'Christmas Day', 'gift', 'Weihnachtsgeschenke', plus 'failed to deliver'.",
     "sub_themes_observed": "gift delivery timing; damaged gift; return",
     "confidence": "low"},
]