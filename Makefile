HASS_ADDON_DIR=/path/to/hass-addons/

package:
	rm -rf voip-dialler-addon
	mkdir voip-dialler-addon
	cp Dockerfile config.yaml start.sh run.py testfile.wav requirements.txt authorized_keys voip-dialler-addon/

install: package
	rm -rf $(HASS_ADDON_DIR)/voip-dialler-addon
	cp -r voip-dialler-addon $(HASS_ADDON_DIR)/voip-dialler-addon

clean:
	rm -f *~
	rm -rf voip-dialler-addon
