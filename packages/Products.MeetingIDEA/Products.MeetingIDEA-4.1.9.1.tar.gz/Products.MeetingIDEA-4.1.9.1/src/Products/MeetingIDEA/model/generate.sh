#!/bin/sh
/srv/archgenxml/bin/archgenxml --cfg generate.conf MeetingIDEA.zargo -o tmp

# only keep workflows
cp -rf tmp/profiles/default/workflows/meetingitemcaidea_workflow ../profiles/default/workflows
cp -rf tmp/profiles/default/workflows/meetingcaidea_workflow ../profiles/default/workflows
rm -rf tmp
