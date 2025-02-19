export function trimString(string) {
  const maxLength = 7
  const trimmedString = string.length > maxLength ? string.substring(0, maxLength) : string
  return trimmedString
}
