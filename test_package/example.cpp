#include <iostream>
#include <libuvc/libuvc.h>

int main() {
    uvc_context_t *context = NULL;
    uvc_error_t res = uvc_init(&context, NULL);
    if (res != UVC_SUCCESS) {
        uvc_perror(res, "uvc_init");
        return res;
    }
    return 0;
}
