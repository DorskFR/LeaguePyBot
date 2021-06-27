from LPBv2.common import WebSocketEventResponse

ready_check_event = WebSocketEventResponse(
    type="UPDATE",
    uri="/lol-champ-select/v1/session",
    data={
    "dodgeData": {
        "dodgerId": 0,
        "state": "Invalid"
    },
    "errors": [],
    "estimatedQueueTime": 212.27200317382812,
    "isCurrentlyInQueue": True,
    "lobbyId": "",
    "lowPriorityData": {
        "bustedLeaverAccessToken": "",
        "penalizedSummonerIds": [],
        "penaltyTime": 0.0,
        "penaltyTimeRemaining": 0.0,
        "reason": ""
    },
    "queueId": 420,
    "readyCheck": {
        "declinerIds": [],
        "dodgeWarning": "None",
        "playerResponse": "None",
        "state": "InProgress",
        "suppressUx": False,
        "timer": 8.0
    },
    "searchState": "Found",
    "timeInQueue": 120.0
})