// Indonesia city → (lat, lon) lookup for natal-chart computation.
// Mirrors zodiac.py: INDONESIA_CITIES, JAKARTA_COORDS, geocode_city.
//
// The full chart (sun/moon/rising) requires an ephemeris library
// (Python used `immanuel`); we'll wire the chart computation in a
// later session — for now this module just exposes the lookup so
// the UI can validate / autocomplete birth-city inputs.

export const JAKARTA_COORDS: readonly [number, number] = [-6.2088, 106.8456];

export const INDONESIA_CITIES: Record<string, readonly [number, number]> = {
  jakarta: [-6.2088, 106.8456],
  bandung: [-6.9175, 107.6191],
  surabaya: [-7.2575, 112.7521],
  medan: [3.5952, 98.6722],
  semarang: [-6.9667, 110.4167],
  makassar: [-5.1477, 119.4327],
  palembang: [-2.9761, 104.7754],
  denpasar: [-8.6705, 115.2126],
  yogyakarta: [-7.7956, 110.3695],
  jogja: [-7.7956, 110.3695],
  malang: [-7.9797, 112.6304],
  bogor: [-6.595, 106.8166],
  depok: [-6.4025, 106.7942],
  tangerang: [-6.1783, 106.6319],
  bekasi: [-6.2349, 106.9896],
  batam: [1.0456, 104.0305],
  pekanbaru: [0.5071, 101.4478],
  padang: [-0.9471, 100.4172],
  manado: [1.4748, 124.8421],
  balikpapan: [-1.2379, 116.8529],
  pontianak: [-0.0263, 109.3425],
  banjarmasin: [-3.3194, 114.5906],
  samarinda: [-0.5022, 117.1536],
  jayapura: [-2.5337, 140.7181],
  ambon: [-3.6955, 128.1814],
  kupang: [-10.1772, 123.607],
  mataram: [-8.5833, 116.1167],
  surakarta: [-7.5755, 110.8243],
  solo: [-7.5755, 110.8243],
  cirebon: [-6.732, 108.5523],
  tasikmalaya: [-7.3506, 108.2172],
  bali: [-8.6705, 115.2126],
};

/**
 * Best-effort city → coords lookup. Returns null if the city isn't in
 * our Indonesia map. (Python had a Nominatim fallback; we'll add a
 * server-side fetch in a later session if needed.)
 */
export function geocodeCity(cityName: string): [number, number] | null {
  const key = cityName.trim().toLowerCase().split(",")[0]?.trim();
  if (!key) return null;
  const hit = INDONESIA_CITIES[key];
  return hit ? [hit[0], hit[1]] : null;
}
