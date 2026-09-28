# Test Plan

| ID | Scenario | Expected |
|---|---|---|
| T01 | Register | Account created |
| T02 | Duplicate registration | 409 |
| T03 | Login | JWT returned |
| T04 | Organizer creates event | 200 |
| T05 | Attendee creates event | 403 |
| T06 | Retrieve events | List returned |
| T07 | Valid RSVP | Stored |
| T08 | Duplicate RSVP | Existing RSVP updated |
| T09 | GOING -> MAYBE | Counts change |
| T10 | MAYBE -> GOING | Counts change |
| T11 | Cancel RSVP | NOT_GOING |
| T12 | Deadline passed | Rejected |
| T13 | Capacity full | Rejected / waitlisted |
| T14 | Simultaneous final-seat requests | Only capacity permits |
| T15 | Waitlist | WAITLISTED record |
| T16 | Announcement | Stored + notification |
| T17 | Unauthorized event edit | 403 |
| T18 | Unauthorized RSVP access | 403 |
| T19 | WebSocket update | Counter changes without refresh |
| T20 | Analytics | Counts calculated |
| T21 | DB unavailable | Graceful API error |
| T22 | WebSocket disconnect | REST still works |
| T23 | Token expiry | 401 |
| T24 | Event cancellation | RSVP blocked |
| T25 | Refresh during RSVP | Database remains source of truth |

## Actual Result / Pass-Fail

Fill these columns during the final demo:

| Test ID | Actual Result | Pass/Fail |
|---|---|---|
| T01-T25 | Record after execution | Fill during testing |
