"use client";

import { useEffect } from "react";
import { checkBackendHealth } from "@/lib/api";

/**
 * BackendWarmup Component
 * 
 * This component pings the backend health endpoint on mount.
 * This is useful for "waking up" free tier services (like Render)
 * as soon as the user loads the application.
 */
export default function BackendWarmup() {
  useEffect(() => {
    // We don't need to do anything with the response,
    // just the act of fetching will wake up the Render service.
    checkBackendHealth()
      .then((ok) => {
        if (ok) {
          console.log("🚀 Backend warmed up and ready");
        }
      })
      .catch(() => {
        // Silently ignore errors, we'll handle them during actual requests
      });
  }, []);

  // This component doesn't render anything
  return null;
}
