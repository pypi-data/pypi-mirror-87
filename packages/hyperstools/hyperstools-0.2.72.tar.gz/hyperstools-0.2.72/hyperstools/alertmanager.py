import requests
import json
import arrow

try:
    import django
    isDjango = True
except ImportError:
    isDjango = False
if isDjango:
    from django.conf import settings
    try:
        alertApi = settings.ALERTMANAGER_API
        isDjango = True
    except django.core.exceptions.ImproperlyConfigured:
        isDjango = False
else:
    pass
def notify(receiver=None,
           interval=60,
           alertname="default_alertname",
           service=None,
           severity=None,
           instance=None,
           job=None,
           user=None,
           summary="default_summary",
           description="default_description"):

    headers = {"Content-Type": "application/json"}
    utctime = arrow.utcnow()
    endtime = utctime.shift(seconds=+interval)
    alertData = {}
    if receiver:
        alertData.setdefault("receiver", receiver)
    alertData.setdefault("startsAt", str(utctime))
    alertData.setdefault("endsAt", str(endtime))
    labels = {
        "alertname": alertname,
    }
    if service:
        labels.setdefault("service", service)
    if severity:
        labels.setdefault("severity", severity)
    if instance:
        labels.setdefault("instance", instance)
    if job:
        labels.setdefault("job", job)
    if user:
        labels.setdefault("user", user)
    annotations = {"summary": summary, "description": description}
    alertData.setdefault("labels", labels)
    alertData.setdefault("annotations", annotations)
    alertData = [alertData]
    data = json.dumps(alertData, ensure_ascii=False)
    response_data = requests.post(url=alertApi, data=data, headers=headers)
    try:
        results = response_data.json()
    except:
        results = {"status": "error"}
    return results


if __name__ == "__main__":
    results = notify(receiver="live-monitoring")
    print(results)