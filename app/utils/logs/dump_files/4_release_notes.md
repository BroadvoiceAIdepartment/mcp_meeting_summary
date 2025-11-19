# Release Notes

## Communicator Android - 25.20

November 17th, 2025

## Introduction
### Overview  
    This release includes:

- Improved contact display and update responsiveness.
- Fixed caller ID stability and visibility issues.
- Enhanced real-time status indicators in internal chats.
- Stability and accuracy improvements across mobile contact details.

Release Version - 25.20

## New features
[BAMA-2008](https://broadvoice-jira.atlassian.net/browse/BAMA-2008) **Display sending status for internal conversations**  
      Users can now see real-time sending status in internal chats, enhancing communication transparency.


## Enhancements
[BAMA-1864](https://broadvoice-jira.atlassian.net/browse/BAMA-1864) **Implement reactive internal and external contact update handling**  
      The contact update system now reacts instantly to changes, keeping contact information current across the platform.


## Bug fixes
[BAMA-1913](https://broadvoice-jira.atlassian.net/browse/BAMA-1913) **Created contacts do not immediately display the Name on incoming calls**  
      The contact display now updates instantly on incoming calls, ensuring users see caller information without delay.

[BAMA-1972](https://broadvoice-jira.atlassian.net/browse/BAMA-1972) **Flickering on user caller ID**  
      The caller ID flickering issue has been resolved, providing a clearer and more stable caller identification experience.

[BAMA-2053](https://broadvoice-jira.atlassian.net/browse/BAMA-2053) **Internal Contact Details Not Updating on Mobile**  
      Internal contact details now update correctly on mobile devices, ensuring users always see the latest contact information.


---

## Communicator iOS - 25.20

November 17th, 2025

## Introduction
### Overview  
    This release includes:

- Improved call setup and audio controls.

Release Version - 25.20

## Bug fixes
[BIMA2-1301](https://broadvoice-jira.atlassian.net/browse/BIMA2-1301) **Audio button incorrectly pre-selected on call initiation**  
      The audio button now defaults correctly during call start, preventing user confusion and streamlining call setup.

[BIMA2-1319](https://broadvoice-jira.atlassian.net/browse/BIMA2-1319) **System messages unarchive group conversations**  
      Group conversations now unarchive properly when system messages are received, improving message management.


---

## Communicator Web - 25.20

November 17th, 2025

## Introduction
### Overview  
    This release includes:

- Improved contact and message information accuracy.
- Enhanced media setup and device display in browsers.
- New real-time messaging and noise cancellation features.
- Better call notifications and user guidance for new chats.

Release Version - 25.20

## New features
[CUU2-2961](https://broadvoice-jira.atlassian.net/browse/CUU2-2961) **Implement optimistic message sending with status display in internal chats**  
      Messages now send optimistically with real-time status updates, enhancing chat responsiveness and user confidence.

[CUU2-3033](https://broadvoice-jira.atlassian.net/browse/CUU2-3033) **[Video] Implement Noise Cancellation (Krisp)**  
      Noise cancellation using Krisp is now integrated into video calls, improving audio clarity for users.


## Enhancements
[CUU2-2965](https://broadvoice-jira.atlassian.net/browse/CUU2-2965) **Empty state for new chats via search bar**  
      An empty state view now appears for new chats initiated through search, guiding users smoothly into conversations.

[CUU2-2977](https://broadvoice-jira.atlassian.net/browse/CUU2-2977) **Contact Duplicates 2nd Phase**  
      Duplicate contact management has been enhanced, reducing clutter and improving contact accuracy.

[CUU2-3020](https://broadvoice-jira.atlassian.net/browse/CUU2-3020) **Adjust incoming call notification when the user is on a call**  
      Incoming call notifications are now better adjusted when users are already on a call, minimizing disruptions.


## Bug fixes
[CUU2-2790](https://broadvoice-jira.atlassian.net/browse/CUU2-2790) **Updated contact name not reflected in message info panel**  
      Updated contact names now appear correctly in message info panels, ensuring accurate communication details.

[CUU2-3048](https://broadvoice-jira.atlassian.net/browse/CUU2-3048) **Message input unblocks for adhoc groups, allowing SMS without 10DLC campaign registration**  
      Message input is now unblocked for ad hoc groups, enabling SMS sending without requiring 10DLC campaign registration.

[CUU2-3057](https://broadvoice-jira.atlassian.net/browse/CUU2-3057) **Audio and video Source/Device are not displayed correctly (Chrome & Firefox)**  
      Audio and video source and device displays are now accurate across Chrome and Firefox browsers, improving media setup.

---

## Internals
[COMAPI-1331](https://broadvoice-jira.atlassian.net/browse/COMAPI-1331) **[Messaging API] Cap conversations limit fetch to 100**  
      The messaging API now limits conversation fetches to 100, optimizing performance and data handling.

[CUU2-3045](https://broadvoice-jira.atlassian.net/browse/CUU2-3045) **[Video] Bugsnag integration**  
      Bugsnag error monitoring has been integrated into video features, enabling proactive issue detection and resolution.

[CUU2-3047](https://broadvoice-jira.atlassian.net/browse/CUU2-3047) **Limit Conversation Polling to 30**  
      Conversation polling frequency has been limited to 30 seconds, balancing real-time updates with system performance.



---

## Conclusions
### Product info
### Feedback form
     Could you send us your feedback so that we can improve our documentation on the release notes, please send us your suggestions here [Feedback form](https://forms.office.com/pages/responsepage.aspx?id=shZr4LsVn0qHKScJqTri8qc_RFxi5XdMrfIOTS65N-9UN1ZBUDdPOUZRRlhRNTVWUFZTSDNaQlRYMS4u&route=shorturl )
