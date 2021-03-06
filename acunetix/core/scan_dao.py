import json
from acunetix.helper.api_call import APICall
from acunetix.config import PROFILES
from acunetix.model.scan import Scan


class ScanDAO:
    def create_scan(target, profile_id, schedule):
        if len(profile_id) > 255:
            return None
        data = {
            "profile_id": profile_id,
            "incremental": False,
            "schedule": schedule,
            "target_id": target.id
        }
        try:
            res = APICall.post_raw('/scans', data)
            response = json.loads(res.text)

            scan_id = res.headers['Location'].split('/')[-1]
            incremental = response['incremental']
            max_scan_time = response['max_scan_time']

            new_scan = Scan(id=scan_id, profile=profile_id, incremental=incremental,
                            max_scan_time=max_scan_time, schedule=schedule, target=target)

            return new_scan
        except:
            return None

    def get_all_scans():
        try:
            response = APICall.get('/scans')
            raw_scans = response['scans']
            scans = []

            for scan in raw_scans:
                id = scan['scan_id']
                profile = scan['profile_id']
                incremental = scan['incremental']
                max_scan_time = scan['max_scan_time']
                next_run = scan['next_run']
                report = scan['report_template_id']
                schedule = scan['schedule']

                new_scan = Scan(id, profile, incremental=incremental,
                                max_scan_time=max_scan_time, next_run=next_run, report=report, schedule=schedule)
                
                scans.append(new_scan)
            
            return scans

        except:
            return []

    def get_scan_by_id(scan_id):
        try:
            scan_id = scan_id.strip()
            scan_id = scan_id.lower()
            if len(scan_id) > 255:
                return None
            scan = APICall.get('/scans/{}'.format(scan_id))
            id = scan['scan_id']
            profile = scan['profile_id']
            incremental = scan['incremental']
            max_scan_time = scan['max_scan_time']
            next_run = scan['next_run']
            report = scan['report_template_id']
            schedule = scan['schedule']

            new_scan = Scan(id, profile, incremental=incremental,
                            max_scan_time=max_scan_time, next_run=next_run, report=report, schedule=schedule)

            return new_scan
        except:
            return None

    def stop_scan(scan):
        return APICall.post_raw('/scans/{}/abort'.format(scan.id))

    def pause_scan(scan):
        return APICall.post_raw('/scans/{}/pause'.format(scan.id))

    def resume_scan(scan):
        return APICall.post_raw('/scans/{}/resume'.format(scan.id))

    def delete_scan(scan):
        id = scan.id
        if len(id) > 255:
            return None
        return APICall.delete_raw('/scans/{}'.format(id))
