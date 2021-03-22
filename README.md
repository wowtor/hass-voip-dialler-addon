Home Assistant SIP Dialler Addon
================================

Addon for [Home Assistant](http://home-assistant.io) to dial a SIP
extension. Can be used, for example, to notify the home owner when an alarm is
triggered.

This addon exposes an URL. A request to this URL is followed by a phone
ringing. When answered, a WAV file is played. The URL can be called from
elsewhere, such as the
[RESTful Command extension](https://www.home-assistant.io/integrations/rest_command/).


Prerequisites
=============

A subscription to a VOIP service.


Setup
=====

Checkout this repository and upload it to a Home Assistant instance, as
described in the
[Addon tutorial](https://developers.home-assistant.io/docs/add-ons/tutorial).

Optionally, enable SSH access. To do this, edit the `authorized_keys` file
to add your public SSH key.

Configure the addon. It requires the following parameters:

- sip_host: a SIP server;
- sip_user
- sip_password
- call_extension: an extension, generally a phone number
- play_file: the WAV file to play fro mthe local filesystem; uploaded to the
  container and must be 16kbit signed mono (single channel)
- call_time_secs: the number of seconds of the call. The dialler will hangup after this many seconds after the call was initiated (including ring time and call time).

Test if it works. Access `http://homeassistant.local:8000/call` in your
browser. If the phone is ringing, it worked.


Usage
=====

The
[RESTful Command extension](https://www.home-assistant.io/integrations/rest_command/)
is installed by default. Follow the instructions to expose the VOIP dialler
service. This involes editing `configuration.yaml`, which can be done using
the [File Editor addon](https://www.home-assistant.io/getting-started/configuration/).

Good luck!
