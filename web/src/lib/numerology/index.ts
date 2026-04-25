// Public barrel for the numerology module. Re-exports everything
// callers typically need: types, the buildProfile orchestrator,
// individual math helpers, and the data dictionaries (under a `data`
// namespace so the call site stays explicit about looking up
// meanings vs computing).

export * from "./core";
export * from "./numbers";
export * from "./cycles";
export * from "./extras";
export * from "./forecast";
export * from "./profile";

// Data dictionaries — exposed via dot path so call sites read like
// `numerology.data.MEANINGS[1]` rather than colliding with helpers.
import * as archetypes from "./data/archetypes";
import * as karmic from "./data/karmic";
import * as letters from "./data/letters";
import * as planes from "./data/planes";
import * as forecastData from "./data/forecast";

export const data = {
  ...archetypes,
  ...karmic,
  ...letters,
  ...planes,
  ...forecastData,
};
