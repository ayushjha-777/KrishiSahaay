export function getErrorMessage(error: any): string {

  // Request timeout
  if (error.code === "ECONNABORTED") {
    return "Request timed out. Please try again.";
  }

  // No internet / backend unreachable
  if (!error.response) {
    return "Unable to connect to the server. Check your internet connection.";
  }

  // Bad request
  if (error.response.status === 400) {
    return "Please upload a valid potato leaf image.";
  }

  // Server error
  if (error.response.status >= 500) {
    return "Server is currently unavailable. Please try again later.";
  }

  return "Something went wrong. Please try again.";
}