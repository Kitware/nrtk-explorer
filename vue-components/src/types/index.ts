export type Vector2<T> = [T, T]
export type Vector3<T> = [T, T, T]
export type Vector4<T> = [T, T, T, T]
export type Vector5<T> = [T, T, T, T, T]
export type Vector6<T> = [T, T, T, T, T, T]

export type ImageMetadata = {
  id: number
  width: number
  height: number
}

export type Annotation = {
  id: number
  category_id: number
  bbox: Vector4<number>
}

export type Category = {
  id: number
  name: string
}

export type ParameterValue = string | number

export type ParameterDescription = {
  type: 'string' | 'integer' | 'float' | 'boolean'
  label: string
  default?: ParameterValue
  options?: ParameterValue[]
}
