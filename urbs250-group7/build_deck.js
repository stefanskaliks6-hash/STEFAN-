// Builds the Group 7 (Office Mid-Rise) summary deck for URBS 250, lecture 6-2 homework.
//   node build_deck.js            -> Group7_Office_MidRise_Summary.pptx
// All numbers come from data/group7_submissions.json; fill that file and re-run.
const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");

const data = JSON.parse(fs.readFileSync(path.join(__dirname, "data/group7_submissions.json"), "utf8"));
const OUT = path.join(__dirname, "Group7_Office_MidRise_Summary.pptx");

// ---- palette: mirrors the course deck (charcoal ground, navy table header, lavender rows) ----
const BG = "1E1E1E";
const WHITE = "FFFFFF";
const MUTED = "A6A6A6";
const ACCENT = "7FA2FF";      // legible blue on charcoal (course uses 003399, too dark on black)
const NAVY = "003399";
const ROW_A = "CDCFE0";
const ROW_B = "E6E7F0";
const CELL_TXT = "1F3B63";
const FONT = "Arial";

// ---- metrics ----
const FIELDS = [
  { key: "lot_m2", label: "Lot Size (m²)", fmt: "m2" },
  { key: "lot_value", label: "Lot Value ($)", fmt: "$" },
  { key: "building_value", label: "Building ($)", fmt: "$" },
  { key: "property_total", label: "Property Total ($)", fmt: "$" },
  { key: "gfa_m2", label: "GFA (m²)", fmt: "m2" },
  { key: "previous_assessment", label: "Previous Assessment ($)", fmt: "$" },
];
const DASH = "—";
const isNum = (v) => typeof v === "number" && Number.isFinite(v);
function fmt(v, kind) {
  if (!isNum(v)) return DASH;
  if (kind === "$") return "$" + Math.round(v).toLocaleString("en-CA");
  if (kind === "m2") return Math.round(v).toLocaleString("en-CA") + " m²";
  if (kind === "ratio") return v.toFixed(2);
  if (kind === "pct") return (v >= 0 ? "+" : "") + (v * 100).toFixed(1) + " %";
  return String(v);
}
const subs = data.submissions;
const fullName = (m) => `${m.first} ${m.last}`;
const subFor = (m) => subs[m.last] || {};

function stats(key) {
  const vals = data.members.map((m) => subFor(m)[key]).filter(isNum);
  if (!vals.length) return { n: 0, avg: null, min: null, max: null };
  return {
    n: vals.length,
    avg: vals.reduce((a, b) => a + b, 0) / vals.length,
    min: Math.min(...vals),
    max: Math.max(...vals),
  };
}
const submitted = data.members.filter((m) => FIELDS.some((f) => isNum(subFor(m)[f.key]))).length;

// ---- deck ----
const pres = new pptxgen();
pres.defineLayout({ name: "COURSE_4x3", width: 10, height: 7.5 });
pres.layout = "COURSE_4x3";
pres.title = "Group 7 – Office Mid-Rise – Summary";
pres.subject = data.course;
pres.author = "URBS 250 Group 7";
pres.theme = { headFontFace: FONT, bodyFontFace: FONT };

pres.defineSlideMaster({
  title: "COURSE_DARK",
  background: { color: BG },
  objects: [
    { text: { text: "URBS 250", options: { x: 4.0, y: 6.95, w: 2.0, h: 0.3, fontFace: FONT, fontSize: 10, color: MUTED, align: "center" } } },
  ],
  slideNumber: { x: 8.9, y: 6.95, w: 0.6, h: 0.3, fontFace: FONT, fontSize: 10, color: MUTED, align: "right" },
});

// Small plan diagram of the mid-rise office typology (site 150' x 400', slab + structured parking).
function drawTypologyPlan(slide, x, y, scale, labels = true) {
  const W = 1.5 * scale, H = 4.0 * scale; // 150' x 400'
  slide.addShape(pres.shapes.RECTANGLE, { x, y, w: W, h: H, fill: { color: BG }, line: { color: MUTED, width: 1, dashType: "dash" }, objectName: "Site boundary" });
  // structured parking (upper part of site)
  slide.addShape(pres.shapes.RECTANGLE, { x: x + 0.12 * W, y: y + 0.05 * H, w: 0.45 * W, h: 0.33 * H, fill: { color: "3A3A3A" }, line: { color: MUTED, width: 0.75 }, objectName: "Parking structure" });
  // office slab
  slide.addShape(pres.shapes.RECTANGLE, { x: x + 0.12 * W, y: y + 0.42 * H, w: 0.62 * W, h: 0.5 * H, fill: { color: ACCENT, transparency: 15 }, line: { color: ACCENT, width: 1 }, objectName: "Office slab" });
  if (!labels) return;
  const lab = { fontFace: FONT, fontSize: 10, color: MUTED, isTextBox: true, margin: 0 };
  slide.addText("150'", { ...lab, x, y: y - 0.3, w: W, h: 0.25, align: "center" });
  slide.addText("400'", { ...lab, x: x - 0.45, y: y + H / 2 - 0.12, w: 0.4, h: 0.25, align: "right" });
  slide.addText("Parking", { ...lab, x: x + 0.12 * W, y: y + 0.05 * H, w: 0.45 * W, h: 0.33 * H, align: "center", valign: "middle", color: "D0D0D0" });
  slide.addText("Office", { ...lab, x: x + 0.12 * W, y: y + 0.42 * H, w: 0.62 * W, h: 0.5 * H, align: "center", valign: "middle", color: "10203F", bold: true });
}

// ---------- Slide 1: cover ----------
{
  const s = pres.addSlide({ masterName: "COURSE_DARK" });
  s.addText("URBS 250  ·  GROUP 7  ·  BUILDING TYPOLOGY", { x: 0.6, y: 0.55, w: 6.2, h: 0.35, fontFace: FONT, fontSize: 12, bold: true, color: ACCENT, charSpacing: 2, isTextBox: true, margin: 0 });
  s.addText("Office Mid-Rise", { x: 0.6, y: 0.95, w: 6.4, h: 0.95, fontFace: FONT, fontSize: 44, bold: true, color: WHITE, isTextBox: true, margin: 0 });
  s.addText("Property assessment summary of our team's submissions", { x: 0.6, y: 1.9, w: 6.2, h: 0.4, fontFace: FONT, fontSize: 16, italic: true, color: "D9D9D9", isTextBox: true, margin: 0 });

  const present = (data.presenting || []).length ? data.presenting : null;
  const heading = present ? "Present today" : "Group members (present today)";
  s.addText(heading, { x: 0.6, y: 2.65, w: 6.2, h: 0.35, fontFace: FONT, fontSize: 16, bold: true, color: WHITE, isTextBox: true, margin: 0 });

  const names = present ? present : data.members.map(fullName);
  const half = Math.ceil(names.length / 2);
  const col = (arr) => arr.map((n, i) => ({ text: n, options: { breakLine: i < arr.length - 1 } }));
  const listOpts = { y: 3.1, w: 3.05, h: 3.5, fontFace: FONT, fontSize: 14, color: "E6E6E6", valign: "top", paraSpaceAfter: 5, isTextBox: true, margin: 0 };
  s.addText(col(names.slice(0, half)), { ...listOpts, x: 0.6 });
  s.addText(col(names.slice(half)), { ...listOpts, x: 3.7 });

  drawTypologyPlan(s, 7.6, 1.25, 1.05);
  s.addText("Typical mid-rise office: 60,000 SF site,\nstructured parking", { x: 6.95, y: 5.65, w: 2.6, h: 0.55, fontFace: FONT, fontSize: 10, color: MUTED, align: "center", isTextBox: true, margin: 0 });

  s.addNotes(
    "Cover sheet. Group 7: Office Mid-Rise. Before presenting, list only the members present today " +
      "(set the \"presenting\" array in data/group7_submissions.json, or delete absent names here)."
  );
}

// ---------- Slide 2: summary table ----------
{
  const s = pres.addSlide({ masterName: "COURSE_DARK" });
  s.addText(
    [
      { text: "Office Mid-Rise  -  ", options: { color: WHITE } },
      { text: "Summary table", options: { color: ACCENT } },
    ],
    { x: 0.5, y: 0.7, w: 9.0, h: 0.8, fontFace: FONT, fontSize: 32, align: "center", isTextBox: true, margin: 0 }
  );

  const hdr = (t) => ({ text: t, options: { bold: true, color: WHITE, fill: { color: NAVY }, fontSize: 15 } });
  const rows = [[hdr(""), hdr("Average"), hdr("Minimum"), hdr("Maximum")]];
  FIELDS.forEach((f, i) => {
    const st = stats(f.key);
    const fill = { color: i % 2 === 0 ? ROW_A : ROW_B };
    const cell = (t, bold = false) => ({ text: t, options: { fill, color: CELL_TXT, bold, fontSize: 14 } });
    rows.push([cell(f.label, true), cell(fmt(st.avg, f.fmt)), cell(fmt(st.min, f.fmt)), cell(fmt(st.max, f.fmt))]);
  });
  s.addTable(rows, {
    x: 0.5, y: 1.85, w: 9.0, colW: [2.7, 2.1, 2.1, 2.1], rowH: 0.62,
    fontFace: FONT, valign: "middle", margin: [0, 0.12, 0, 0.12],
    border: { type: "solid", pt: 1, color: WHITE },
    objectName: "Summary table",
  });

  const nNote = submitted
    ? `Based on ${submitted} of ${data.members.length} member submissions. Average = arithmetic mean; blanks excluded.`
    : `Awaiting team data: 0 of ${data.members.length} submissions entered.`;
  s.addText(
    [
      { text: nNote, options: { breakLine: true } },
      { text: "Source: Ville de Montréal, rôle d'évaluation foncière (current roll; previous roll for “Previous Assessment”)." },
    ],
    { x: 0.5, y: 6.25, w: 9.0, h: 0.55, fontFace: FONT, fontSize: 10, color: MUTED, isTextBox: true, margin: 0 }
  );
  s.addNotes(
    "Min, average and max across our team's Office Mid-Rise properties. Property Total = Lot Value + Building. " +
      "GFA = gross floor area. Previous Assessment = total value on the previous assessment roll."
  );
}

// ---------- Slides 3+: one example per member ----------
data.members.forEach((m) => {
  const d = subFor(m);
  const s = pres.addSlide({ masterName: "COURSE_DARK" });
  s.addText(fullName(m), { x: 0.5, y: 0.5, w: 9.0, h: 0.6, fontFace: FONT, fontSize: 30, bold: true, color: WHITE, isTextBox: true, margin: 0 });
  s.addText(d.address || "Address: to be added", {
    x: 0.5, y: 1.12, w: 9.0, h: 0.4, fontFace: FONT, fontSize: 15, italic: true, color: d.address ? ACCENT : MUTED, isTextBox: true, margin: 0,
  });

  // photo frame (left)
  s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 1.8, w: 4.2, h: 4.6, fill: { color: "2A2A2A" }, line: { color: "555555", width: 1, dashType: "dash" }, objectName: "Photo frame" });
  drawTypologyPlan(s, 2.1, 2.35, 0.65, false);
  s.addText("Paste property photo / Street View here", { x: 0.6, y: 5.55, w: 4.0, h: 0.6, fontFace: FONT, fontSize: 11, color: MUTED, align: "center", isTextBox: true, margin: 0 });

  // data table (right)
  const far = isNum(d.gfa_m2) && isNum(d.lot_m2) && d.lot_m2 > 0 ? d.gfa_m2 / d.lot_m2 : null;
  const chg = isNum(d.property_total) && isNum(d.previous_assessment) && d.previous_assessment > 0 ? d.property_total / d.previous_assessment - 1 : null;
  const lines = [
    ...FIELDS.map((f) => [f.label, fmt(d[f.key], f.fmt)]),
    ["Floors (storeys)", isNum(d.floors) ? String(d.floors) : DASH],
    ["Year built", isNum(d.year_built) ? String(d.year_built) : DASH],
    ["FAR (GFA ÷ lot)", fmt(far, "ratio")],
    ["Change vs previous roll", fmt(chg, "pct")],
  ];
  const rows = lines.map(([k, v], i) => {
    const fill = { color: i % 2 === 0 ? ROW_A : ROW_B };
    const derived = i >= FIELDS.length + 2;
    return [
      { text: k, options: { fill, color: CELL_TXT, bold: true, italic: derived } },
      { text: v, options: { fill, color: CELL_TXT, align: "right", italic: derived } },
    ];
  });
  s.addTable(rows, {
    x: 5.0, y: 1.8, w: 4.5, colW: [2.55, 1.95], rowH: 0.46,
    fontFace: FONT, fontSize: 13, valign: "middle", margin: [0, 0.1, 0, 0.1],
    border: { type: "solid", pt: 1, color: WHITE },
    objectName: "Property data",
  });
  s.addText("Italic rows are calculated: FAR = GFA ÷ lot size; change = property total ÷ previous assessment − 1.", {
    x: 5.0, y: 6.45, w: 4.5, h: 0.4, fontFace: FONT, fontSize: 9, color: MUTED, isTextBox: true, margin: 0,
  });
  s.addNotes(`Example submitted by ${fullName(m)} (Office Mid-Rise). Source: Ville de Montréal assessment roll.`);
});

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote", OUT, `(${submitted}/${data.members.length} submissions with data)`));
