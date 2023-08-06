#!python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys

import babel

# Print full name of short language code, e.g.
# returns "Deutsch" for "de".

lang_code = sys.argv[1]
try:
    lo = babel.Locale.parse(lang_code)
    print(lo.get_display_name())
except Exception:
    print(lang_code)
