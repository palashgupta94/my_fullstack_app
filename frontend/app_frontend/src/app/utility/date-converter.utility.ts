

  export function getISTISOString(): string {
    const indiaTime = new Date().toLocaleString("en-US", { timeZone: "Asia/Kolkata" });
    return new Date(indiaTime).toISOString();
  }

