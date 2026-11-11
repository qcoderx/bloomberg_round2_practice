# Matchmaking Service

This service places users into skill-based lobbies, maintains the waiting queue, pairs compatible users, renews active queue entries, expires old entries, and reports lobby activity.

## Run the tests

```text
python -m unittest discover -v
```

## Customer reports

- A customer on a slow network was added to the same lobby twice.
- A customer joined a Python lobby and was paired with another user who had none of the lobby's listed skills.
- A customer remained in the queue beyond the advertised 90 seconds and was matched without joining again.
- A two-person lobby showed three customers waiting at the same time.

The individual reports are in the `tickets` directory.

