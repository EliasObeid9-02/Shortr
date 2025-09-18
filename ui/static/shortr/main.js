function copyToClipboard() {
  const shortUrlInput = document.getElementById("short-url-display");
  shortUrlInput.select();
  shortUrlInput.setSelectionRange(0, 99999); // For mobile devices
  document.execCommand("copy");
}
