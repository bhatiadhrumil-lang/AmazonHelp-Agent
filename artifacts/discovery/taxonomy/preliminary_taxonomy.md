# Preliminary intent taxonomy (Phase 1C, TASK 8) - DRAFT FOR HUMAN VALIDATION

- Built from **203 clusters** / **43,550 clustered points** (49,621 noise excluded from taxonomy for now).
- **PRELIMINARY and emergent.** Number of leaves (below) is what the clusters suggest; it is not a preset target and will change after human review.
- **Not a truth claim.** These are evidence-based readings of cluster representative messages. HDBSCAN clusters are not ground truth, and no accuracy statement is made.

## Top-level view (by kind)

| kind | label | n clusters | n points | share of clustered |
|---|---|---|---|---|
| intent | cluster appears to express a real customer goal | 125 | 20005 | 45.9% |
| artifact | conversation-closure / template turn - NOT an intent; needs the conversation layer | 46 | 4218 | 9.7% |
| sentiment | venting / accusation - NOT a goal; carries an underlying issue elsewhere in the thread | 7 | 337 | 0.8% |
| contextual | reading depends on the rest of the thread | 22 | 16959 | 38.9% |
| ood | out-of-domain / off-topic chatter | 3 | 2031 | 4.7% |

## Intent area map (PRELIMINARY, emergent groupings)

| possible_parent_intent | n clusters | n points | share | kind | member families |
|---|---|---|---|---|---|
| Needs re-clustering | 1 | 12267 | 28.2% | contextual | megacluster_unclear |
| Delivery & shipping | 39 | 7079 | 16.2% | intent | carrier_unreachable;carrier_unreachable;delivery_carrier;delivery_carrier;delivery_carrier;delivery_carrier;delivery_carrier;delivery_carrier;delivery_carrier;delivery_carrier;delivery_carrier;delivery_date_change;delivery_delay;delivery_delay;delivery_delay;delivery_delay;delivery_delay;delivery_delay;delivery_driver;delivery_driver;delivery_estimate;delivery_estimate;delivery_tracking;delivery_tracking;delivery_tracking;delivery_tracking;delivery_urgency;gift_delivery;item_missing;item_missing;item_missing;misdelivery;misdelivery;not_dispatched;package_damaged;shipping_speed;shipping_speed;shipping_speed;shipping_speed |
| Conversation closure (artifact) | 46 | 4218 | 9.7% | artifact | ack_done;ack_done;ack_done;ack_thanks;ack_thanks;ack_thanks;ack_thanks;ack_thanks;ack_thanks;ack_thanks;ack_thanks;ack_thanks;ack_thanks;ack_thanks;ack_thanks;ack_thanks;ack_thanks;ack_thanks;ack_thanks;ack_thanks;ack_thanks;ack_thanks;ack_thanks;ack_thanks;ack_willdo;ack_willdo;ack_willdo;ack_willdo;ack_willdo;ack_willdo;empathy_farewell;empathy_farewell;resolution_thanks;resolution_thanks;resolution_thanks;template_affirm;template_affirm;template_affirm;template_affirm;template_affirm;template_neg;template_neg;template_neg;template_neg;template_time;template_time |
| Verification / information flow | 15 | 3300 | 7.6% | contextual | detail_provided;detail_provided;detail_provided;detail_provided;detail_provided;detail_provided;detail_provided;detail_provided;detail_provided;detail_provided;detail_provided;detail_provided;detail_provided;detail_provided;detail_provided |
| Agent / support experience | 10 | 2088 | 4.8% | intent | agent_escalation;agent_escalation;agent_escalation;bot_vs_human;complaint_service_quality;complaint_service_quality;complaint_service_quality;complaint_service_quality;complaint_service_quality;complaint_service_quality |
| Orders & fulfilment | 10 | 2052 | 4.7% | intent | cancel_order;cancel_order;order_status;order_status;order_status;refund_request;refund_request;replacement_request;return_process;return_process |
| Out-of-domain / conversational | 3 | 2031 | 4.7% | ood | off_topic_chat;off_topic_chat;off_topic_chat |
| Support progress: waiting / nudge | 9 | 1618 | 3.7% | intent | cs_team_no_response;cs_team_no_response;cs_team_no_response;next_step_guidance;resolution_pending;resolution_pending;resolution_pending;resolution_pending;resolution_pending |
| Amazon devices & apps | 8 | 1470 | 3.4% | intent | connectivity;device_issue;device_issue;device_issue;echo_alexa;echo_alexa;fire_tv;kindle_app |
| Account & settings | 1 | 1044 | 2.4% | intent | account_login |
| Products & defects | 9 | 970 | 2.2% | intent | preorder;preorder;preorder;product_defect;product_defect;product_defect;product_defect;product_question;product_question |
| Support progress: waiting / nudge | 5 | 744 | 1.7% | contextual | status_update_request;status_update_request;time_estimate_query;waiting_status;waiting_status |
| Shopping & catalogue | 7 | 701 | 1.6% | intent | price_change;price_change;region_mismatch;region_mismatch;shipping_cost;stock_availability;stock_availability |
| Contacting support | 6 | 670 | 1.5% | intent | contact_callback_request;contact_channel;contact_channel;contact_phone_issue;contact_phone_issue;third_party_contact |
| Payments & billing | 5 | 657 | 1.5% | intent | charge_inquiry;gift_card;payment_method;prime_charge;prime_charge |
| Context-dependent / unclear | 1 | 648 | 1.5% | contextual | transitional |
| Digital content & streaming | 7 | 507 | 1.2% | intent | music;prime_video;prime_video;prime_video;prime_video;prime_video;prime_video |
| Marketplace & sellers | 3 | 373 | 0.9% | intent | seller_issue;seller_issue;seller_issue |
| Verification / information flow | 6 | 368 | 0.9% | intent | link_issue;link_issue;link_issue;link_issue;link_issue;verify_fax |
| Promotions & offers | 3 | 320 | 0.7% | intent | contest_promo;contest_promo;promo_code |
| Sentiment / venting (not a customer goal) | 6 | 297 | 0.7% | sentiment | fraud_accusation;negative_frustration;negative_frustration;negative_frustration;negative_frustration;negative_frustration |
| Security / account safety | 1 | 50 | 0.1% | intent | phish_email |
| Complaints & sentiment | 1 | 40 | 0.1% | sentiment | false_advertising |
| Community & reviews | 1 | 38 | 0.1% | intent | review_q |

## Reading notes

### 1. Bigger than expected share of *non-intent* clusters
Only **125** of the 203 clusters are read as expressing a customer goal; the rest are conversation-closure artifacts, sentiment/venting, thread-contextual turns, or OOD chatter. In this Twitter-DM support data the social layer is big: a human validator should confirm this before designing triage.

### 2. Delivery & shipping dominates the customer-goal volume
Tracking/delay/date/carrier/driver/misdelivery/damage/speed clusters together are the largest *intent* family by clustered points (several clusters >1000: e.g. cluster 7's megacluster, 156, 146, 198). Delivery sub-themes need the split review in split_candidates.csv.

### 3. Orders & fulfilment (refund/replacement/return) is the second large block
Refund and replacement status clusters (189, 183, 187) plus return-pickup (46, 188) are frequent. Note the distinction kept between *refund request/status* (goal) and the historical *response* (how AmazonHelp replied) - response behaviour is intentionally NOT encoded in the labels.

### 4. Conversation-closure and waiting/status clusters dominate the *artifact* half
46 clusters are acknowledgments, commitments, polarity/date answers or status waits (incl. clusters 0-6, 110-135, 158-159). These are merge candidates (see merge_candidates.csv).

### 5. What is NOT in the taxonomy
- 49,621 noise points - sampled and classified separately (see noise_analysis.md);
- No named 'AUTO-CLARIFY-ESCALATE' decisions anywhere - automation policy is a separate concern from intents and was not derived here;
- No cluster renamed as a *final* intent - every label carries 'Likely/Conversation/…' style wording pending human validation.