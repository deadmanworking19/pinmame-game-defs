# Installed companion light mapping

Literal complete `vpmMapLights` subroutine from retained core.vbs,
lines 2607–2621. File SHA-256:
`a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69`.

```vb
Sub vpmMapLights(aLights)
	Dim obj, str, ii, idx
	For Each obj In aLights
		idx = obj.TimerInterval
		If IsArray(Lights(idx)) Then
			str = "Lights(" & idx & ") = Array("
			For Each ii In Lights(idx) : str = str & ii.Name & "," : Next
			ExecuteGlobal str & obj.Name & ")"
		ElseIf IsObject(Lights(idx)) Then
			Lights(idx) = Array(Lights(idx),obj)
		Else
			Set Lights(idx) = obj
		End If
	Next
End Sub
```

The address is TimerInterval regardless of TimerEnabled. Repeated addresses
create multiple rendering helpers for one circuit. The object name is used to
assemble that helper array and does not supply the public lamp address.
