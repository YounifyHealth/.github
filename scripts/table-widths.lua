-- Give Markdown pipe tables explicit relative widths so LuaLaTeX wraps cells
-- instead of allowing wide programme tables to run off the page.

local function weight(header)
  local h = string.lower(header or "")
  if h == "id" or h == "wp" or h == "pr" or h == "gate" or h == "size" or h == "order" or h == "class" then
    return 0.62
  end
  if string.find(h, "lead") or string.find(h, "owner") or string.find(h, "reviewer") or string.find(h, "actor") or h == "from" or h == "to" then
    return 0.82
  end
  if string.find(h, "title") or string.find(h, "work package") or string.find(h, "current conclusion") or string.find(h, "planning consequence") then
    return 1.75
  end
  if string.find(h, "finding") or string.find(h, "outcome") or string.find(h, "recommendation") or string.find(h, "failure") or string.find(h, "responsibility") or string.find(h, "treatment") or string.find(h, "plan") then
    return 2.15
  end
  if string.find(h, "dependencies") or string.find(h, "evidence") or string.find(h, "repository") or string.find(h, "readiness") then
    return 1.20
  end
  return 1.0
end

function Table(tbl)
  local headers = {}
  if tbl.head and tbl.head.rows and #tbl.head.rows > 0 then
    for i, cell in ipairs(tbl.head.rows[1].cells) do
      headers[i] = pandoc.utils.stringify(cell.contents)
    end
  end
  local total = 0
  local weights = {}
  for i, spec in ipairs(tbl.colspecs) do
    weights[i] = weight(headers[i])
    total = total + weights[i]
  end
  if total == 0 then
    return tbl
  end
  for i, spec in ipairs(tbl.colspecs) do
    tbl.colspecs[i] = {spec[1], 0.96 * weights[i] / total}
  end
  return tbl
end
