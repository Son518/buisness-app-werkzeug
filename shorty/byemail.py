from nylas import APIClient

nylas = APIClient(
    "1rn7dql5wn17g16kpq1bngjk6",
    "cbwl6munoro37mvd23p39l9gf",
    "enSSJD52X0uyWsWIZEijt2ApOwTzYd",
)
draft = nylas.drafts.create()
draft.subject = "With Love, from Nylas"
draft.body = "This email was sent using the Nylas Email API. Visit https://nylas.com for details."

draft.to = [{'name': 'My Nylas Friend', 'email': 'wangnaixu88@gmail.com'}]

draft.send()