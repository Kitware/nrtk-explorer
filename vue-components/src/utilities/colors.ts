import type { Vector3 } from '../types'

function uint8(value: number): number {
  if (value < 0) {
    return 0
  } else if (value > 1) {
    return 255
  } else {
    return Math.round(value * 255)
  }
}

function hex(value: number): string {
  const result = uint8(value).toString(16)
  return result.length < 2 ? '0' + result : result
}

function isColor(mapped: MapValue<number>): mapped is Vector3<number> | Vector3<number> {
  return Array.isArray(mapped)
}

type MapValue<T> = Vector3<T> | Vector3<T> | T

export function toUint8<T extends MapValue<number>>(mapped: T): T {
  if (isColor(mapped)) {
    return mapped.map((v) => uint8(v)) as T
  } else {
    return uint8(mapped as number) as T
  }
}

export function toHex<T extends MapValue<number>>(mapped: T): string {
  if (isColor(mapped)) {
    return mapped.map((v) => hex(v)).join('')
  } else {
    return hex(mapped as number)
  }
}

export function toRGB<T extends MapValue<number>>(mapped: T): string {
  if (isColor(mapped)) {
    return mapped.map((v) => uint8(v)).join(',')
  } else {
    return `${uint8(mapped as number)}`
  }
}
