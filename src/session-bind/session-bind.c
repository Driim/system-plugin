/*
 * Copyright (c) 2018 Samsung Electronics Co., Ltd.
 *
 * Licensed under the Apache License, Version 2.0 (the License);
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */

#include <stdio.h>
#include <errno.h>
#include <sys/mount.h>
#include <tzplatform_config.h>

// For compatibility, Using hard-coded path
#define LEGACY_APPS_DIR "/opt/usr/apps"
#define LEGACY_CONTENTS_DIR "/opt/usr/media"

int main(int argc, char *argv[])
{
	int r;
	const char *user_app;
	const char *user_content;

	user_app = tzplatform_getenv(TZ_USER_APP);
	r = mount(user_app, LEGACY_APPS_DIR, NULL, MS_BIND, NULL);
	if (r < 0) {
		fprintf(stderr, "user app bind mount failed - %d\n", errno);
		return r;
	}

	user_content = tzplatform_getenv(TZ_USER_CONTENT);
	r = mount(user_content, LEGACY_CONTENTS_DIR, NULL, MS_BIND, NULL);
	if (r < 0) {
		fprintf(stderr, "user content bind mount failed - %d\n", errno);
		return r;
	}

	return 0;
}
