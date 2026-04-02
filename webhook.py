from discord import SyncWebhook

webhook = SyncWebhook.from_url("YOUR_WEBHOOK_URL_HERE")
webhook.send("Hello World!")
