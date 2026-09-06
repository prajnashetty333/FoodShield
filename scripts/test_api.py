import requests

base = 'http://127.0.0.1:8000/api'
results = []

def check_endpoint(name, expected_status, path, params=None):
    try:
        r = requests.get(base + path, params=params or {}, timeout=10)
        ok = r.status_code == expected_status
        status = 'PASS' if ok else 'FAIL'
        results.append((name, r.status_code, ok))
        print(f'[{status}] {name}: {r.status_code}')
        return r
    except Exception as e:
        results.append((name, 'ERR', False))
        print(f'[FAIL] {name}: {e}')
        return None

check_endpoint('Overview 200', 200, '/overview')
check_endpoint('Countries options 200', 200, '/countries/options')
check_endpoint('Country Japan/Wheat/2023 200', 200, '/countries/analysis', {'country': 'Japan', 'commodity': 'Wheat', 'year': 2023})
check_endpoint('Country invalid 404', 404, '/countries/analysis', {'country': 'INVALID_COUNTRY', 'commodity': 'Wheat', 'year': 2023})
check_endpoint('Country valid/invalid commodity 404', 404, '/countries/analysis', {'country': 'Japan', 'commodity': 'Kale', 'year': 2023})
check_endpoint('Commodities list 200', 200, '/commodities')
check_endpoint('Commodity analysis Wheat 200', 200, '/commodities/analysis', {'commodity': 'Wheat'})
check_endpoint('Commodity analysis invalid 404', 404, '/commodities/analysis', {'commodity': 'Kale'})
check_endpoint('Shock Japan/Wheat/2023/rank1 200', 200, '/shocks/analysis', {'country': 'Japan', 'commodity': 'Wheat', 'year': 2023, 'rank': 1})
check_endpoint('Shock Japan/Wheat/2023/rank2 200', 200, '/shocks/analysis', {'country': 'Japan', 'commodity': 'Wheat', 'year': 2023, 'rank': 2})
check_endpoint('Shock Japan/Wheat/2023/rank3 200', 200, '/shocks/analysis', {'country': 'Japan', 'commodity': 'Wheat', 'year': 2023, 'rank': 3})
check_endpoint('Replacement Japan/Wheat/2023 200', 200, '/replacement/analysis', {'country': 'Japan', 'commodity': 'Wheat', 'year': 2023, 'rank': 1})
check_endpoint('Sensitivity 200', 200, '/sensitivity/analysis')
check_endpoint('Policy 200', 200, '/policy')
check_endpoint('Methodology 200', 200, '/methodology')

print()
passed = sum(1 for r in results if r[2])
print(f'TOTAL: {passed}/{len(results)} tests passed')
