# Traffic Analytics Analysis - Bug Identification

## The "Fake Visits" Issue
The current implementation in `analytics.py` tracks visits using the following method:

```python
def track_visit_once_per_session():
    if st.session_state.get("_av_tracked"):
        return
```

### Why this over-counts traffic:
1. **Streamlit Execution Model**: Any time a user refreshes the page (F5), closes the background tab and restores it, or visits from a new tab, Streamlit wipes the `session_state` completely and establishes a new WebSocket connection. **Each page refresh = 1 new unique visit**.
2. **Bot/Crawler Traffic**: Most basic uptime monitors, link preview generators (like WhatsApp/Slack sharing), and web crawlers load the site. If they execute Javascript, they will trigger a new Streamlit session. Since they start without a cookie or history, every single ping from a bot counts as a new visit.
3. **No Client Fingerprinting**: Upstash simply runs `["INCR", "visits:ap_public:..."]`. There is no IP logging, cookie storage, or LocalStorage flag to deduplicate visits across multiple sessions from the same user/machine.

## The Indexing Logic
Reviewed `get_stats()` indexing slices:
```python
desktop_daily = [parse_val(r) for r in results[2:32]]
mobile_daily = [parse_val(r) for r in results[32:62]]
```
This correctly pulls exactly 30 days of data and sums them correctly via `desktop_30d = sum(desktop_daily)`. **There is no off-by-one math error** multiplying traffic.

## Conclusion
The high traffic numbers are likely "inflated" by:
1. You and other users refreshing the page repeatedly to see data updates.
2. Web scrapers, search indexing bots, and vulnerability scanners hitting the public URL.
3. Uptime Monitors (if active).
