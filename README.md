# DESCRIPTION
Small flask app to act as a proxy between the Flipper Zero app and Home Assistant, 
since HA does't expose a way to ask for multiple specific entities (either only one or all of them) and the resulting json response is huge (over 50kB). 
This proxy will return to the Flipper only the requested entities.

# HOW TO USE
rename the config_example.json to config.json and edit it:
- "host" should point to the HA endpoint,
- add as many kv pairs as needed, where the key is the entity_id on HA and the value is the custom name used on the request/response from/to the Flipper.
