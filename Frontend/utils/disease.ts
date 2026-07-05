export function formatDiseaseName(name: string) {
  return name
    .replace("Potato___", "")
    .replace("_", " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());
}