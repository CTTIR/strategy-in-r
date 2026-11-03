-- Raw HTML emitted by tables and images must also satisfy EPUB's XML syntax.
-- Preserve table markup and values, omit empty style attributes, and use native
-- image nodes so the EPUB writer produces XML-compatible image attributes.
if not FORMAT:match('epub') then return {} end
local void = {area=true, base=true, br=true, col=true, embed=true, hr=true,
  img=true, input=true, link=true, meta=true, param=true, source=true,
  track=true, wbr=true}

local function normalize_tag(tag)
  local name, rest = tag:match('^<([%a][%w:_-]*)(.*)>$')
  if not name then return tag end
  local attrs, pos = {}, 1
  while pos <= #rest do
    local first, last, key = rest:find('^%s*([%a_:][%w:_.-]*)', pos)
    if not first then break end
    pos = last + 1
    local _, space_end = rest:find('^%s*', pos)
    pos = space_end + 1
    local value = '""'
    if rest:sub(pos, pos) == '=' then
      pos = pos + 1
      local _, end_space = rest:find('^%s*', pos)
      pos = end_space + 1
      local quote = rest:sub(pos, pos)
      if quote == '"' or quote == "'" then
        local close = rest:find(quote, pos + 1, true)
        if not close then return tag end
        value = rest:sub(pos, close)
        pos = close + 1
      else
        local first_value, last_value = rest:find('^[^%s]+', pos)
        if not first_value then return tag end
        value = '"' .. rest:sub(first_value, last_value):gsub('"', '&quot;') .. '"'
        pos = last_value + 1
      end
    end
    if not (key == 'style' and (value == '""' or value == "''")) then
      attrs[#attrs + 1] = ' ' .. key .. '=' .. value
    end
  end
  return '<' .. name .. table.concat(attrs) .. ((void[name:lower()] or rest:match('/%s*$')) and ' />' or '>')
end

local function xml_syntax(el)
  if el.format ~= 'html' then return nil end
  -- The pattern consumes quoted strings intact, including embedded angle brackets.
  local text, pos, parts = el.text, 1, {}
  while pos <= #text do
    local start = text:find('<%a', pos)
    if not start then parts[#parts + 1] = text:sub(pos); break end
    parts[#parts + 1] = text:sub(pos, start - 1)
    local finish, quote = start + 1, nil
    while finish <= #text do
      local c = text:sub(finish, finish)
      if quote then
        if c == quote then quote = nil end
      elseif c == '"' or c == "'" then quote = c
      elseif c == '>' then break end
      finish = finish + 1
    end
    if finish > #text then parts[#parts + 1] = text:sub(start); break end
    parts[#parts + 1] = normalize_tag(text:sub(start, finish))
    pos = finish + 1
  end
  el.text = table.concat(parts)
  return el
end
local function inline(el)
  if el.format == 'html' and el.text:match('^%s*<img[%s>]') then
    local blocks = pandoc.read(el.text, 'html').blocks
    if #blocks == 1 and (blocks[1].t == 'Plain' or blocks[1].t == 'Para') then
      return blocks[1].content
    end
  end
  return xml_syntax(el)
end
-- Bookdown emits resolved cross-references as raw anchor tags. Native links
-- let Pandoc route those targets to the correct split XHTML chapter.
local function links(inlines)
  local out, i = pandoc.List(), 1
  while i <= #inlines do
    local el = inlines[i]
    local target = el.t == 'RawInline' and el.format == 'html'
      and el.text:match('^<a href="#([^"]+)">$')
    if target then
      local content, j = pandoc.List(), i + 1
      while j <= #inlines do
        local next_el = inlines[j]
        if next_el.t == 'RawInline' and next_el.format == 'html'
          and next_el.text == '</a>' then break end
        content:insert(next_el)
        j = j + 1
      end
      if j <= #inlines then
        out:insert(pandoc.Link(content, '#' .. target))
        i = j + 1
      else out:insert(el); i = i + 1 end
    else out:insert(el); i = i + 1 end
  end
  return out
end
return {RawBlock=xml_syntax, RawInline=inline, Inlines=links}
