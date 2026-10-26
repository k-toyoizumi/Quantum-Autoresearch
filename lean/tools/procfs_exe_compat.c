#define _GNU_SOURCE
#include <dlfcn.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

/*
 * Temporary workaround for this executor's split PID/procfs namespace.
 * Lean asks readlink("/proc/<pid>/exe") for its own executable, but that PID
 * is not addressable in the mounted procfs here. The override only redirects
 * numeric /proc/<pid>/exe lookups and leaves all other readlink calls intact.
 * It does not modify Lean, Lake, Mathlib, or the proof kernel.
 */
ssize_t readlink(const char *path, char *buf, size_t size) {
  static ssize_t (*real_readlink)(const char *, char *, size_t);
  if (!real_readlink) real_readlink = dlsym(RTLD_NEXT, "readlink");

  if (path && strncmp(path, "/proc/", 6) == 0) {
    const char *p = path + 6;
    if (*p >= '0' && *p <= '9') {
      while (*p >= '0' && *p <= '9') ++p;
      if (strcmp(p, "/exe") == 0) {
        const char *override = getenv("LEAN_PROC_EXE_OVERRIDE");
        if (override && *override) {
          size_t n = strlen(override);
          if (n > size) n = size;
          memcpy(buf, override, n);
          return (ssize_t)n;
        }
      }
    }
  }
  return real_readlink(path, buf, size);
}
