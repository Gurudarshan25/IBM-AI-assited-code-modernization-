# What I checked, and what the agent got wrong

## What the agent got wrong
- **It fixed the division but almost left the report floored.** Changing `//` to `/` in
  `fleet_summary` fixed the number, but `print_report` still printed it with `"%d%%"`, so the
  nightly report would have shown 59.67% as 59%. The sweep caught it; it now prints one decimal.
- **It changed behaviour in code nobody asked it to touch.** While "modernizing" the unused
  `format_percent`, it switched `%d` (round down) to `:.0f` (round to nearest). Harmless today
  because nothing calls it, but it is a behaviour change dressed up as a style change.
- **It said it was finished at 9 of 11.** After the code fixes it reported success, but
  `verify.py` still failed on `analyze.py` and these notes. Running the check myself is what showed
  the job was not done.
- **Its risk score is graded on the data it was built from.** The 0.85 AUC in `analyze.py` is
  in-sample (120 cars, 26 breakdowns), so it is optimistic. It needs checking against new data
  before anyone trusts the exact number.

## What I checked before I accepted its work
- Ran `pytest` before the change (3 of 3 failing) and after (11 of 11 passing).
- Ran the **new** tests against the **original** code: 10 of 11 failed. So the tests really catch
  the old bugs, they are not just written to pass.
- The 80% rule is untouched: `SERVICE_INTERVAL_KM = 15000` and `WARN_AT_PERCENT = 80` are unchanged,
  `settings.cfg` is unchanged in git, and `test_threshold_boundary_is_unchanged` checks that exactly
  12,000 km is flagged and 11,999 km is not.
- The wear bug is fixed: `wear_percent(14900, 15000)` returns 99.3 (it returned 0), and the car
  VOS-4471 is flagged.
- The miles bug: 100 km now reads 62.1 miles, not 160.9 (`MILES_PER_KM` was 1.609, which is km
  per mile, not miles per km).
- Ran `python verify.py` until every line said PASS, and ran the real report on
  `fleet_sample.json` to see that VOS-7788 (no reading) no longer crashes it.

## What the data actually said
- The factor that matters most is **km since the last service** (broken-down cars average 11,678 km
  vs. 7,261 km; correlation 0.40). Next come **average daily km** (160 vs. 131; 0.25) and **load
  factor** (0.60 vs. 0.51; 0.22).
- **Total mileage does not predict a breakdown.** Both groups average about 53,300 km on the
  odometer (correlation 0.00). **Age** is the same story: 5.9 years in both groups. "Older,
  higher-mileage cars break down" is not what this data says.
- 9 of the 26 breakdowns happened before the car reached 12,000 km (80%) since its service, so
  the 80% rule alone would never have flagged them. The risk score in `analyze.py` ranks cars that
  are driven hard and loaded heavily higher, so they get looked at earlier.
